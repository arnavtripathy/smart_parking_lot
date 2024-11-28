from django.db import models

class ParkingUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    car_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username