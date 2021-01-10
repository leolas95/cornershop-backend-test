from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
# Create your views here.
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
            return redirect(reverse('profile'))
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
            return redirect(reverse('profile'))
        context = {'form': form}
        return render(request, 'signup.html', context)


class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')


class LoginEmployeeView(LoginView):
    template_name = 'login.html'

