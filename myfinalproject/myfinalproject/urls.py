"""myfinalproject URL Configuration

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
from museos import views
from django.contrib.auth.views import logout
from django.contrib.auth.views import login
from django.views.static import serve
from django.views.generic import TemplateView


urlpatterns = [
    url(r'static/(.*)$', serve, {'document_root': 'templates/miplantilla'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.inicio, name='Página principal'),
    url(r'^museos/$', views.todos, name='Página todos los museos'),
    url(r'^about$', TemplateView.as_view(template_name='miplantilla/about.html')),
    url(r'^logout$', logout),
    url(r'^login$', login),
    url(r'^accounts/profile/', views.login_exito, name="Login hecho"),
]
