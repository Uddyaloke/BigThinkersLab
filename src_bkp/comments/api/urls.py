from __future__ import unicode_literals

from django.contrib import admin
from django.urls import path, re_path, include
from .views import (
	CommentCreateAPIView,
	CommentDetailAPIView,
	CommentListAPIView,
	)

app_name = 'comments-api'

urlpatterns = [
	re_path(r'^$', CommentListAPIView.as_view(), name='list'),
	re_path(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    re_path(r'(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # re_path(r'(?P<id>\d+)/delete/$', comment_delete, name='delete')
]