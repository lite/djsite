# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Marker

class MarkerAdmin(admin.ModelAdmin):
    list_display = ['phone', 'latitude', 'longitude','message']

admin.site.register(Marker, MarkerAdmin)

