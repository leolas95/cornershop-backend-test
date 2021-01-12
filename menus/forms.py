from django import forms


class CreateMenuForm(forms.Form):
    date = forms.DateField()

    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', [])
        super(CreateMenuForm, self).__init__(*args, **kwargs)

        for i, option in enumerate(options, 1):
            key = f'option{i}'
            self.fields[key] = forms.CharField(max_length=100, label=option[key])
