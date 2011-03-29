# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Package, Lesson

class PackageAdmin(admin.ModelAdmin):
    list_display = ['tag', 'date', 'summary']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['path', 'version', 'link', 'package']
    raw_id_fields = ['package',]

admin.site.register(Package, PackageAdmin)
admin.site.register(Lesson, LessonAdmin)

