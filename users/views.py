from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from users.forms import CreateEmployeeForm
from users.models import Employee


class SignUpManagerView(View):
    def get(self, request):
        form = CreateEmployeeForm()
        context = {'form': form}
        return render(request, 'signup.html', context)

    def post(self, request):
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.save()

            auth_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, auth_user)
            return redirect(reverse('profile', kwargs={'employee_id': user.pk}))
        context = {'form': form}
        return render(request, 'signup.html', context)


class ProfileView(View):
    def get(self, request, employee_id):
        employee = Employee.objects.filter(pk=employee_id)
        if not employee.exists():
            return HttpResponse('User doesn\'t exists')

        employee = employee.first()

        return render(request, 'profile.html')

