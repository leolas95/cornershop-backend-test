from django import forms

from menus.models import Menu


class CreateMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('date', 'option1', 'option2', 'option3', 'option4')
