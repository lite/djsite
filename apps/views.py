from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    if not request.user.is_authenticated(): 
           return HttpResponseRedirect('accounts/login/?next=%s' % request.path)
    return render_to_response('index.html', context_instance=RequestContext(request))
