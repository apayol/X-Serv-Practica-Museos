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
    url(r'^admin/', include(admin.site.urls)),
    url(r'static/(.*)$', serve, {'document_root': 'templates/miplantilla'}),
    url(r'^$', views.inicio, name='Página principal'),
    url(r'^museos$', views.todos, name='Página todos los museos'),
    url(r'^museos/(\d+)$', views.museo, name='Página particular museo'),
    url(r'^about$', TemplateView.as_view(template_name='miplantilla/about.html'), name='Info de la app'),
    url(r'^logout$', views.logout_form, name='Hacer logout'),
    url(r'^login$', views.login_form, name='Hacer login'),
    url(r'^(.+)/xml', views.xml_usuario, name="XML de la página de usuario"),
    url(r'^(.+)/json$', views.json_usuario, name='JSON de la página de usuario'),
    url(r'^xml$', views.xml_inicio, name="XML de la página de inicio"),
    url(r'^json$', views.json_inicio, name="JSON de la página de inicio"),
    url(r'^rss$', views.rss_comentarios, name="RSS de comentarios"),
    url(r'^(.*)$', views.usuario, name="Página particular de usuario"),
]
