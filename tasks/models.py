from django.db import models
from django.core.validators import RegexValidator
from users.models import Users

alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alpha')

state_choices = (('To Do', 'To Do'), ('Done', 'Done'))

# Create your models here.

class User_Tasks (models.Model):
    description = models.CharField(
        max_length=500, verbose_name="Description", blank=True, validators=[alpha])
    state = models.CharField(max_length=20, verbose_name="State", default='To Do', choices=state_choices)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


    def __str__(self):
        return '%s %s' % (self.description)
