from __future__ import unicode_literals
from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView


from comments.forms import CommentForm
from comments.models import Comment

from hitcount.views import HitCountDetailView

from hitcount.models import HitCount
from posts.models import Post
from postgroups.models import Postgroup


def home_list(self, request):
	today = timezone.now().date()
	qs_postgrp = HitCount.objects.annotate(postgrp_count=Count('hit_count_postgrp_generic_relation')).order_by('-hits')

	context = {
		"object_list": qs_postgrp,
		"title": "List",
		"today": today,
	}

	return render(request, 'base.html', context)

