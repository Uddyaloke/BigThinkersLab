from __future__ import unicode_literals

from django.contrib import admin
from django.urls import path, re_path, include
from .views import (
	comment_thread,
	comment_delete
	)

app_name = 'comments'

urlpatterns = [
    re_path(r'(?P<id>\d+)/$', comment_thread, name='thread'),
    re_path(r'(?P<id>\d+)/delete/$', comment_delete, name='delete')
]