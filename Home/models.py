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
        return " Name : " + self.name

class Crew(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, default='')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    status = models.BooleanField(default='1')
    role = models.CharField(max_length=100, default='crew')
    ship =  models.CharField(max_length=50, default='')
    added_user = models.CharField(max_length=50, default='')

    def __str__(self):
        return " Crew : " + self.name + " , Ship : " + str(self.ship)+ " , Status : " + str(self.status)


class Port(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, default='')
    location = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, default='')
    status = models.BooleanField(default='1')
    role = models.CharField(max_length=100, default='port')
    added_user = models.CharField(max_length=50, default='')

    def __str__(self):
        return " Port : " + self.name + " , Loctaion : " + str(self.location)+ " , Status :"  + str(self.status)

class Ship(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default='')
    source = models.CharField(max_length=150, default='')
    destination = models.CharField(max_length=150, default='')
    password = models.CharField(max_length=50, default='123456')
    status = models.BooleanField(default='1')
    role = models.CharField(max_length=100, default='ship')
    added_user = models.CharField(max_length=50, default='')

    def __str__(self):
        return " Ship : " + self.name + " , Status : " + str(self.status)

class Container(models.Model):
    containerNumber = models.CharField(max_length=100)
    source = models.CharField(max_length=150, default='')
    destination = models.CharField(max_length=150, default='')
    ship = models.CharField(max_length=150, default='')
    date = models.DateField(null=True, blank=True)
    collect_status = models.BooleanField(default='0')
    drop_status = models.BooleanField(default='0')
    status = models.BooleanField(default='1')
    added_user = models.CharField(max_length=50, default='')

    def __str__(self):
        return " Container Number : " + self.containerNumber + " , Ship : " + str(self.ship) + " , Status : " + str(self.status)
