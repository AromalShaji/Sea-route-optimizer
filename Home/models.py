from email.policy import default
from django.db import models

# Create your models here.


class useradmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    status = models.BooleanField(default='1')
    role = models.CharField(max_length=100, default='admin')

    def __str__(self):
        return self.name
