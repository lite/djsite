#coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
    
class RegisterForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
    email = forms.EmailField(label=_('Email'))
    mobile = forms.CharField(label=_('Mobile'))