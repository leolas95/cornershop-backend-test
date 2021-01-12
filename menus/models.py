import uuid

from django.db import models

from users.models import Employee


class Menu(models.Model):
    date = models.DateField(unique=True)


class Option(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=100)

    def __str__(self):
        return self.option

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('menu', 'option'), name='menu_option_unique')
        ]


class MenuSelection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(Employee, on_delete=models.CASCADE)
    option = models.OneToOneField(Option, on_delete=models.CASCADE, related_name='selection')
