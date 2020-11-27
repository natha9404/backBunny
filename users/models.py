from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alpha')

# Create your models here.
class OwnUser (models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Name User", blank=True, validators=[alpha])

    def __str__(self):
        return self.name