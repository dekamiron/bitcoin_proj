from django.db import models
# Create your models here.
import datetime
from django.core.validators import MinLengthValidator


class Hash(models.Model):
    value = models.CharField(max_length=64, validators=[MinLengthValidator(64)])
    is_confirmed = models.BooleanField(default=False)
    user_email = models.EmailField()

    def __str__(self):
        return '{} | is_confirmed: {}'.format(self.value, self.is_confirmed)
