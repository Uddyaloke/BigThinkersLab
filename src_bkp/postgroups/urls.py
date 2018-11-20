from __future__ import unicode_literals

from django.contrib import admin
from django.urls import path, re_path, include
from .views import (
	post_group_list,
	post_group_create,
	post_group_detail,
	post_group_tag_list,
	post_group_update,
	post_group_delete,
	PostgroupLikeToggle,
	PostgroupLikeAPIToggle
	)

app_name = 'post-groups'

urlpatterns = [
    re_path(r'^$', post_group_list, name='list'),
    re_path(r'^create$', post_group_create, name='post_create'),
    path('<slug:slug>/', post_group_detail, name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/like/$', PostgroupLikeToggle.as_view(), name='like-toggle'),
    re_path(r'^api/(?P<slug>[\w-]+)/like/$', PostgroupLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('<slug:slug>/edit/', post_group_update, name='update'),
    path('<slug:slug>/delete/', post_group_delete, name='post_delete'),
    re_path(r'^tags/(?P<slug>[\w-]+)/$', post_group_tag_list, name='tag_list')
]