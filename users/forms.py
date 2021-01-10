from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Employee


class CreateEmployeeForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name')
