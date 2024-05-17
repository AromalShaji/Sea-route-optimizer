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
    status = models.BooleanField(default='1')
    role = models.CharField(max_length=100, default='crew')
    ship = models.CharField(max_length=50, default='', null=True)
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
    
class RoutePrediction(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    predicted_start_time = models.DateTimeField()
    predicted_end_time = models.DateTimeField()
    predicted_source = models.CharField(max_length=150)
    predicted_destination = models.CharField(max_length=150)

    def __str__(self):
        return f"Route Prediction for {self.ship.name}"

class Container(models.Model):
    containerNumber = models.CharField(max_length=100)
    source = models.CharField(max_length=150, default='')
    destination = models.CharField(max_length=150, default='')
    ship = models.CharField(max_length=150, default='')
    collect_status = models.BooleanField(default='0')
    drop_status = models.BooleanField(default='0')
    status = models.BooleanField(default='1')
    added_user = models.CharField(max_length=50, default='')

    def __str__(self):
        return " Container Number : " + self.containerNumber + " , Ship : " + str(self.ship) + " , Status : " + str(self.status)


class RouteInput(models.Model):
    lon_st = models.FloatField()
    lat_st = models.FloatField()
    lon_de = models.FloatField()
    lat_de = models.FloatField()
    stTime = models.CharField(max_length=100)
    eTime = models.CharField(max_length=100)
    generation_count = models.IntegerField()
    pop_size = models.IntegerField()
    offspring = models.IntegerField()
    lon_min = models.IntegerField()
    lon_max = models.IntegerField()
    lat_min = models.IntegerField()
    lat_max = models.IntegerField()
    draft = models.FloatField()