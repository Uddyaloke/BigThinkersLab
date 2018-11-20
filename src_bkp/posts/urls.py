from __future__ import unicode_literals

from django.contrib import admin
from django.urls import path, re_path, include
from .views import (
	post_list,
	post_create,
	post_detail,
	post_tag_list,
	post_update,
	post_delete,
	PostLikeToggle,
	PostLikeAPIToggle
	)

app_name = 'posts'

urlpatterns = [
    re_path(r'^$', post_list, name='list'),
    re_path(r'^create$', post_create, name='post_create'),
    re_path(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
    re_path(r'^api/(?P<slug>[\w-]+)/like/$', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('<slug:slug>/edit/', post_update, name='update'),
    path('<slug:slug>/delete/', post_delete, name='post_delete'),
    re_path(r'^tags/(?P<slug>[\w-]+)/$', post_tag_list, name='tag_list')
]