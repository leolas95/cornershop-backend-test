from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
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
            user.is_superuser = True
            user.save()
            return HttpResponse(f"{user.username}")
        context = {'form': form}
        return render(request, 'signup.html', context)
