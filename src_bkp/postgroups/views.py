
from __future__ import unicode_literals
from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView
from django.views.generic.base import RedirectView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from taggit.utils import _parse_tags


from comments.forms import CommentForm
from comments.models import Comment

from hitcount.views import HitCountDetailView

from posts.models import Post
from .models import Postgroup
from .forms import PostGroupForm
# from .utils import get_read_time

# Create your views here.


def post_group_create(request):
	# return HttpResponse("<h1>Create</h1>")
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	if not request.user.is_authenticated:
		raise Http404

	form = PostGroupForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		# print(form.cleaned_data.get("title"))
		instance.user = request.user
		instance.save()
		form.save_m2m()
		tag_list = _parse_tags(strip_tags(request.POST.get('teaser')))
		instance.tags.add(*tag_list)
		messages.success(request, "Post Group Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"form": form,
	}

	return render(request, 'post_group_form.html', context)

def post_group_detail(request, slug=None):
	instance = get_object_or_404(Postgroup, slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id,
	}

	form = CommentForm(request.POST or None, initial=initial_data)

	if form.is_valid() and request.user.is_authenticated:
		# print(form.cleaned_data)
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")

		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type = content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj
						)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments

	post_list = Postgroup.objects.filter(id=instance.id).values_list('posts', flat=True)
	relevant_posts = Post.objects.filter(id__in=post_list)

	common_tag_model_ids = Postgroup.tags.most_common()[:5].values_list('postgroup', flat=True)

	trending_instances = Postgroup.objects.filter(id__in=common_tag_model_ids)[:5]

	common_tag_post_model = Post.tags.most_common()[:5].values_list('post', flat=True)

	trending_post_instances = Post.objects.filter(id__in=common_tag_post_model)[:5]

	context = {
		"title": instance.title,
		"instance": instance,
		"relevant_posts": relevant_posts,
		"trending_instances": trending_instances,
		"trending_post_instances": trending_post_instances,
		"share_string": share_string,
		"comments": comments,
		"comment_form": form,
	}
	return render(request, 'post_group_detail.html', context)


class PostgroupLikeToggle(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		obj = get_object_or_404(Postgroup, slug=slug)
		url_ = obj.get_absolute_url()
		user = self.request.user
		if user.is_authenticated:
			if user in obj.likes.all():
				obj.likes.remove(user)
			else:
				obj.likes.add(user)
		return url_


class PostgroupLikeAPIToggle(APIView):
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, slug=None, format=None):
		obj = get_object_or_404(Postgroup, slug=slug)
		url_ = obj.get_absolute_url()
		user = self.request.user
		updated = False
		liked = False
		if user.is_authenticated:
			if user in obj.likes.all():
				liked = False
				obj.likes.remove(user)
			else:
				liked = True
				obj.likes.add(user)
				updated = True

		data = {
			"updated": updated,
			"liked": liked
		}
		return Response(data)


def post_group_list(request):
	today = timezone.now().date()
	queryset_list = Postgroup.published_postGroups.active() # .order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Postgroup.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)| 
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.get_page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver first page
		queryset = paginator.get_page(1)
	except EmptyPage:
		# if page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	common_tag_model_ids = Postgroup.tags.most_common()[:5].values_list('postgroup', flat=True)

	trending_instances = Postgroup.objects.filter(id__in=common_tag_model_ids)[:5]

	common_tag_post_model = Post.tags.most_common()[:5].values_list('post', flat=True)

	trending_post_instances = Post.objects.filter(id__in=common_tag_post_model)[:5]

	context = {
		"object_list": queryset,
		"trending_instances": trending_instances,
		"trending_post_instances": trending_post_instances,
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, 'post_group_list.html', context)

def post_group_tag_list(request, slug=None):
	today = timezone.now().date()
	queryset_list = Postgroup.published_postGroups.active() # .order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		tag_id = Postgroup.tags.filter(slug=slug).values_list('postgroup', flat=True)
		queryset_list = Postgroup.objects.filter(id__in=tag_id)

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)| 
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.get_page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver first page
		queryset = paginator.get_page(1)
	except EmptyPage:
		# if page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	common_tag_model_ids = Postgroup.tags.most_common()[:5].values_list('postgroup', flat=True)

	trending_instances = Postgroup.objects.filter(id__in=common_tag_model_ids)[:5]

	common_tag_post_model = Post.tags.most_common()[:5].values_list('post', flat=True)

	trending_post_instances = Post.objects.filter(id__in=common_tag_post_model)[:5]

	context = {
		"object_list": queryset,
		"trending_instances": trending_instances,
		"trending_post_instances": trending_post_instances,
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, 'post_group_list.html', context)

def post_group_update(request, slug=None):
	# return HttpResponse("<h1>Update</h1>")
	# return render(request, 'index.html', context)
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Postgroup, slug=slug)
	form = PostGroupForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		form.save_m2m()
		tag_list = _parse_tags(request.POST.get('teaser'))
		instance.tags.add(*tag_list)
		# message success
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())


	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request, 'post_group_form.html', context)
	

def post_group_delete(request, slug=None):
	# return HttpResponse("<h1>Delete</h1>")	
	# context = {
	# 	"title": "Delete"
	# }
	# return render(request, 'index.html', context)
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Postgroup, slug=slug)
	instance.delete()
	messages.success(request, "Post Successfully Deleted")
	return redirect("post-groups:list")





class PostMixinDetailView(object):
    """
    Mixin to same us some typing.  Adds context for us!
    """
    model = Postgroup

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Postgroup.objects.all()[:5]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context


class IndexView(PostMixinDetailView, TemplateView):
    template_name = 'postgroups/index.html'


class PostDetailJSONView(PostMixinDetailView, DetailView):
    template_name = 'postgroups/postgroup_ajax.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PostDetailJSONView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)


class PostDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view.
    """
    pass


class PostCountHitDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True

