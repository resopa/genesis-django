from django.shortcuts import render
from django.views.generic.base import TemplateView

class CorePageView(TemplateView):
    template_name = "core/home.html"