from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class DasboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html" 