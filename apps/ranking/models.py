from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50,)
    
class Score(models.Model):
    game = models.ForeignKey(Game, related_name='score')
    player = models.CharField(max_length=50,)
    score = models.IntegerField()
    date = models.DateTimeField(null = True)
    