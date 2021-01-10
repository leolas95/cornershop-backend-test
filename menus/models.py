from django.db import models

# Create your models here.


class Menu(models.Model):
    date = models.DateField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
