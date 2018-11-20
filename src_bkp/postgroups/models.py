from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown
from comments.models import Comment
from taggit.managers import TaggableManager
from taggit.models import Tag

from hitcount.models import HitCount, HitCountMixin
from posts.models import Post


class PostGroupManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostGroupManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
	# return "%s/%s" %(instance.id, filename)
	# PostModel = instance.__class__
	new_id = Postgroup.objects.order_by("id").last().id + 1
	return "%s/%s" %(new_id, filename)

class Postgroup(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE,
		default=1)
	posts = models.ManyToManyField(Post)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, 
		null=True, 
		blank=True,
		height_field="height_field", 
		width_field="width_field")
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='postgroup_likes')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	teaser = models.CharField(max_length=100, blank=True, null=True)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, 
		auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, 
		auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, 
		auto_now_add=False)

	hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_postgrp_generic_relation')

	objects = models.Manager()
	published_postGroups = PostGroupManager()

	tags = TaggableManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# return "/posts/%s" %(self.id)
		return reverse("post-groups:detail", kwargs={"slug": self.slug})

	# def get_api_url(self):
	# 	# return "/posts/%s" %(self.id)
	# 	return reverse("posts-api:detail", kwargs={"slug": self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]

	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

	@property
	def view_count(self):
		instance = self
		qs = HitCount.objects.filter_by_instance(self).values('hits')
		if qs:
			for hit_count in qs:
				new_hit_count = hit_count['hits']
				return new_hit_count
		return 0

	@property
	def hitcount(self):
		instance = self
		qs = HitCount.objects.filter(postgroup=self)
		return qs	

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(self)
		return qs	

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

	def get_like_url(self):
		# return "/posts/%s" %(self.id)
		return reverse("post-groups:like-toggle", kwargs={"slug": self.slug})

	def get_api_like_url(self):
		# return "/posts/%s" %(self.id)
		return reverse("post-groups:like-api-toggle", kwargs={"slug": self.slug})

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Postgroup.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

	# if instance.content:
	# 	html_string = instance.get_markdown()
	# 	read_time_var = get_read_time(html_string)
	# 	instance.read_time = read_time_var
	


pre_save.connect(pre_save_post_receiver, sender=Postgroup)


