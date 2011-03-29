from django.db import models

class Marker(models.Model):
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(null = True)
    latitude = models.DecimalField(max_digits=18, decimal_places=10, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=10, null=True)
    message = models.CharField(max_length=100)