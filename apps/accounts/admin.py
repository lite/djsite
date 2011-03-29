# -*- coding: utf-8 -*-
from django.contrib import admin

from models import School, Grade, Classes, UserProfile

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name',]

class GradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'school',]
    raw_id_fields = ['school',]

class ClassesAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', ]
    raw_id_fields = ['grade',]
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['mobile','user','classes', ]
    raw_id_fields = ['user','classes']
    
    
admin.site.register(School, SchoolAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

