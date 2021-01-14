import uuid

from django.db import models
from django.urls import reverse

from users.models import Employee


class Menu(models.Model):
    date = models.DateField(unique=True)


class Option(models.Model):
    """Model to store an option, and the menu it's related to."""

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=100)

    def __str__(self):
        return self.option

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('menu', 'option'), name='menu_option_unique')
        ]


class MenuSelection(models.Model):
    """Model to save the menu selection of a member of the slack workspace."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slack_user_id = models.CharField(max_length=20)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    option = models.OneToOneField(Option, on_delete=models.CASCADE, related_name='selection', null=True)

    def get_absolute_url(self):
        return reverse('select_menu_option', kwargs={'selection_uuid': self.id})
