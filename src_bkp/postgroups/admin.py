from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Postgroup

class PostGroupModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp", "tag_list"]
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["title", "content"]

	class Meta:
		model = Postgroup

	def get_queryset(self, request):
		return super(PostGroupModelAdmin, self).get_queryset(request).prefetch_related('tags')

	def tag_list(self, obj):
		return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Postgroup, PostGroupModelAdmin)