from django.db import models

class Package(models.Model):
    tag = models.IntegerField()
    date = models.DateTimeField(null = True)
    summary = models.CharField(max_length=50,)
    
class Lesson(models.Model):
    package = models.ForeignKey(Package, related_name='Lesson')
    version = models.CharField(max_length=20,)
    summary = models.CharField(max_length=50,)
    link = models.CharField(max_length=250,)
    path = models.CharField(max_length=250,)
    