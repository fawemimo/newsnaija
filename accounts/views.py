from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DasboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html" 