from django import forms

from menus.models import Menu, Option, MenuSelection


class CreateMenuForm(forms.Form):
    date = forms.DateField()

    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', [])
        super(CreateMenuForm, self).__init__(*args, **kwargs)

        for i, option in enumerate(options, 1):
            key = f'option{i}'
            self.fields[key] = forms.CharField(max_length=100, label=option[key])


class MenuForm(forms.ModelForm):
    options = forms.ModelChoiceField(
        queryset=Option.objects.none(),
        widget=forms.RadioSelect
    )

    class Meta:
        model = Menu
        fields = ('options',)

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        self.fields['options'].queryset = self.instance.options
