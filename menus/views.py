from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import CreateView

from menus.forms import CreateMenuForm


class CreateMenuView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = CreateMenuForm
    template_name = 'create_menu.html'
