# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ['headline', 'content', 'reporter','date']

admin.site.register(Report, ReportAdmin)

