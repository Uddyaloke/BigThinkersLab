"""trydjango2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import (
    login_view, 
    register_view, 
    logout_view
    )

from postgroups import views

# from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^comments/', include('comments.urls', namespace='comments')),
    # re_path(r'^posts/', include('posts.urls', namespace='posts')),
    re_path(r'^login/', login_view, name='login'),
    re_path(r'^logout/', logout_view, name='logout'),

    # re_path(r'^/hitcount/$', views.IndexView.as_view(), name="index"),

    re_path(r'^generic-detail-view-ajax/(?P<pk>\d+)/$',
        views.PostDetailJSONView.as_view(),
        name="ajax"),
    re_path(r'^hitcount-detail-view/(?P<pk>\d+)/$',
        views.PostDetailView.as_view(),
        name="detail"),
    re_path(r'^hitcount-detail-view-count-hit/(?P<pk>\d+)/$',
        views.PostCountHitDetailView.as_view(),
        name="detail-with-count"),

    re_path(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

    re_path(r'^register/', register_view, name='register'),
    re_path(r'^posts/', include('posts.urls', namespace='posts')),
    re_path(r'^postgroups/', include('postgroups.urls', namespace='post-groups')),
    re_path(r'^api/auth/token/', obtain_jwt_token),
    re_path(r'^api/users/', include('accounts.api.urls', namespace='users-api')),
    re_path(r'^api/comments/', include('comments.api.urls', namespace='comments-api')),
    re_path(r'^api/posts/', include('posts.api.urls', namespace='posts-api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    


