from django.db import models
from django import forms
from django.contrib.auth.models import User
   
from django.utils.translation import ugettext_lazy as _

class School(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)

    def __unicode__(self):
        return self.name
    
class Grade(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    school = models.ForeignKey(School, related_name='Grade', verbose_name=_('School'))
    
    def __unicode__(self):
        return self.name
    
class Classes(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    grade = models.ForeignKey(Grade, related_name='Classes', verbose_name=_('Grade'))

    def __unicode__(self):
        return self.name

# child, primary, junior high, high, youth
# elementary, junior middle school,senior middle school, university
#nursery, primary,secondary|junior high, senior high, college
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name = "profile")
    
    mobile = models.CharField(max_length = 15, blank = False, null=True)
    classes = models.ForeignKey(Classes, related_name='UserProfile', null=True, verbose_name=_('Classes'))
    