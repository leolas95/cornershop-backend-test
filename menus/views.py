from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView

from menus.forms import CreateMenuForm
from menus.models import Menu


class CreateMenuView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = CreateMenuForm
    template_name = 'create_menu.html'

    def get_success_url(self):
        return reverse('detail_menu', kwargs={'pk': self.object.id})


class DetailMenuView(LoginRequiredMixin, DetailView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'detail.html'
