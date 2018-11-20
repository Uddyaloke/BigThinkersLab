from __future__ import unicode_literals

from django.contrib import admin
from django.urls import path, re_path, include
from .views import (
	PostCreateAPIView,
	PostDeleteAPIView,
	PostDetailAPIView,
	PostListAPIView,
	PostUpdateAPIView,
	)

app_name = 'posts-api'

urlpatterns = [
    re_path(r'^$', PostListAPIView.as_view(), name='list'),
    re_path(r'^create$', PostCreateAPIView.as_view(), name='create'),
    # re_path(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
]