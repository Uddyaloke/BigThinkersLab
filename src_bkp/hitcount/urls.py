# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path, re_path, include

from hitcount.views import HitCountJSONView

app_name = 'hitcount'

urlpatterns = [
    re_path(r'^hit/ajax/$', HitCountJSONView.as_view(), name='hit_ajax'),
]
