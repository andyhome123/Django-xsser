"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', 'core.views.test', name='test'),
    url(r'^$', 'core.views.showAllProject'),
    url(r'^login/$', 'account.views.login', name='login'),
    url(r'^logout/$', 'account.views.logout', name='logout'),
    url(r'^register/$', 'account.views.register', name='register'),
    url(r'^c/$', 'core.views.createProject', name='create'),
    url(r'^cc/$', 'core.views.projectDetail', name='detail'),
    url(r'^show/$', 'core.views.showAllProject', name='show'),
    url(r'^api/$', 'core.views.projectApi', name='api'),
    url(r'^info/$', 'core.views.projectInfo', name='info'),
    url(r'^js/$', 'core.views.projectJs', name='js'),
    url(r'^change/(?P<id>.{36})$', 'core.views.projectChange', name='change'),
    url(r'^delete/(?P<id>.{36})$', 'core.views.projectDelete', name='delete'),


]
