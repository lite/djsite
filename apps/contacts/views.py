from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.core.urlresolvers import reverse

from datetime import datetime

from apps.accounts.models import School

def index(request):
    # users = User.objects.filter(username__iexact=username)
    schools = School.objects.all()
    return render_to_response('contacts/index.html', {'schools':schools}, context_instance=RequestContext(request))
   