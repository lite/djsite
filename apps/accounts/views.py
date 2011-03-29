from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils.translation import ugettext_lazy as _

from models import UserProfile
from forms import LoginForm, RegisterForm

from apps.accounts.models import School, Classes

def register(request):
    errors = []
    schools = School.objects.all()
    if request.method=="POST":
        form = RegisterForm(data = request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            users = User.objects.filter(username__iexact=username)
            if not users:
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                user=User.objects.create_user(username,email,password)
                if user is not None:
                    user.save()
                    profile = UserProfile()
                    profile.user = user
                    profile.mobile = form.cleaned_data["mobile"]
                    profile.classes = Classes.objects.get(pk=request.POST['classesid'])
                    profile.save()
                    success = _login(request,username, password)
                    if success:
                        if request.POST['next']:
                            return HttpResponseRedirect(request.POST['next'])
                        else:
                            return HttpResponseRedirect('/')
                    else:
                        errors += [_("Sorry, that's not a valid username or password")]
                else:
                    errors += [_("Sorry, create user failed.")]
            else:
                errors += [_("Sorry, user has been existed.")]
    else:
        form = RegisterForm()
         
    return render_to_response("accounts/register.html",{'form':form, 'errors':errors, 'schools': schools },context_instance=RequestContext(request))
    
#import pdb
def login(request):
    errors = []
    if request.method == 'POST':
        #pdb.set_trace()
        form = LoginForm(data = request.POST)
        if form.is_valid():
            success = _login(request,form.cleaned_data["username"],form.cleaned_data["password"])
            if success:
                if request.POST['next']:
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect('/')
            else:
                errors += [_("Sorry, that's not a valid username or password")]
        
    else:
        form = LoginForm()
        
    return render_to_response("accounts/login.html", {'form':form, 'errors':errors}, context_instance=RequestContext(request))
    
def _login(request,username,password):
    ret=False
    user=authenticate(username=username,password=password)
    if user:
        auth_login(request,user)
        ret=True
    return ret
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
    