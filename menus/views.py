from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from menus.forms import CreateMenuForm
from menus.models import Menu, Option, MenuSelection


class CreateMenuView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'users:login'
    form_class = CreateMenuForm
    template_name = 'create.html'

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        form = CreateMenuForm()
        return render(request, 'create.html', {'form': form})

    @staticmethod
    def get_options(post_data):
        options = []
        for key, value in post_data.items():
            if key.startswith('option'):
                options.append({key: value})
        return options

    def post(self, request):
        form = CreateMenuForm(request.POST, options=self.get_options(request.POST))
        if form.is_valid():
            date = form.cleaned_data['date']
            menu = Menu.objects.create(date=date)

            # Create options for the menu
            options_to_create = []
            for option in form.cleaned_data:
                if not option.startswith('option'):
                    continue
                options_to_create.append(Option(menu=menu, option=form.cleaned_data[option].capitalize()))
            Option.objects.bulk_create(options_to_create)

            return redirect(reverse('menus:detail_menu', kwargs={'pk': menu.id}))

        return render(request, 'create.html', {'form': form})


class DetailMenuView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Menu
    login_url = 'users:login'
    context_object_name = 'menu'
    template_name = 'detail.html'

    def test_func(self):
        return self.request.user.is_staff


class ListMenuView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Menu
    login_url = 'users:login'
    context_object_name = 'menus'
    template_name = 'list.html'

    def test_func(self):
        return self.request.user.is_staff


class ListSelectionsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MenuSelection
    login_url = 'users:login'
    context_object_name = 'selections'
    template_name = 'list_selections.html'

    def test_func(self):
        return self.request.user.is_staff

