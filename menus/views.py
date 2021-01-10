from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from menus.forms import CreateMenuForm
from menus.models import Menu


class CreateMenuView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = 'login'
    form_class = CreateMenuForm
    template_name = 'create.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('detail_menu', kwargs={'pk': self.object.id})


class DetailMenuView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Menu
    login_url = 'login'
    context_object_name = 'menu'
    template_name = 'detail.html'

    def test_func(self):
        return self.request.user.is_staff


class ListMenuView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Menu
    login_url = 'login'
    context_object_name = 'menus'
    template_name = 'list.html'

    def test_func(self):
        return self.request.user.is_staff

