from __future__ import unicode_literals

from django.contrib import admin

from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp", "tag_list"]
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["title", "content"]

	class Meta:
		model = Post

	def get_queryset(self, request):
		return super(PostModelAdmin, self).get_queryset(request).prefetch_related('tags')

	def tag_list(self, obj):
		return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Post, PostModelAdmin)

