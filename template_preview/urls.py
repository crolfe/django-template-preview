from django.conf.urls import url
from .views import TemplateListView, email_template_render_view

urlpatterns = [
    url(r'^(?P<template_name>\w+)$', email_template_render_view,
        name='template-detail'),
    url(r'^$', TemplateListView.as_view(), name='template-list'),
]
