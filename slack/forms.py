from django import forms

from menus.models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('option1', 'option2', 'option3', 'option4', 'date')
