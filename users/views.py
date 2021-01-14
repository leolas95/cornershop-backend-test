from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.forms import CreateEmployeeForm


class SignUpManagerView(View):
    def get(self, request):
        form = CreateEmployeeForm()
        context = {'form': form}
        return render(request, 'signup.html', context)

    def post(self, request):
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()

            auth_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, auth_user)
            return redirect(reverse('users:profile'))
        context = {'form': form}
        return render(request, 'signup.html', context)


class SignUpEmployeeView(View):
    def get(self, request):
        form = CreateEmployeeForm()
        context = {'form': form}
        return render(request, 'signup.html', context)

    def post(self, request):
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            form.save()

            auth_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, auth_user)
            return redirect(reverse('users:profile'))
        context = {'form': form}
        return render(request, 'signup.html', context)


class ProfileView(LoginRequiredMixin, View):
    login_url = 'users:login'

    @staticmethod
    def get(request):
        return render(request, 'profile.html')


class LoginEmployeeView(LoginView):
    template_name = 'login.html'

