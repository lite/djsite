# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Game, Score

class GameAdmin(admin.ModelAdmin):
    list_display = ['name',]

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['game', 'player', 'score',]
    raw_id_fields = ['game',]

admin.site.register(Game, GameAdmin)
admin.site.register(Score, ScoreAdmin)

