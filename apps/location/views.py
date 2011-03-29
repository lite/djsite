from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import datetime
from models import Marker
from forms import MarkerForm

from django.utils.translation import ugettext_lazy as _

def index(request):
    markers = Marker.objects.all().order_by('-date')[:10]
    return render_to_response('location/index.html', {'markers':markers}, context_instance=RequestContext(request))
    
def showmarker(request, marker_id):
    marker = Marker.objects.get(pk=marker_id)
    if marker:
        if int(marker.latitude)>180:
            marker.message = _("Can not get the GPS information.")
        else:
            marker.message = "%.4f, %.4f"%(marker.latitude, marker.longitude)
    
    return render_to_response('location/showmarker.html', {"marker":marker}, context_instance=RequestContext(request))
    
def addmarker(request):
    if request.method == 'POST':
        form = MarkerForm(request.POST)
        if form.is_valid():
            marker = Marker() 
            marker.phone = form.cleaned_data.get("phone")
            marker.latitude = form.cleaned_data.get("latitude", "32.0")
            marker.longitude = form.cleaned_data.get("longitude", "118.0")
            marker.message = form.cleaned_data.get("message", "")
            marker.date = datetime.now()
            marker.save()
            return HttpResponseRedirect(reverse('location:index'))
    else:
        form = MarkerForm()

    return render_to_response('location/addmarker.html', {'form':form}, context_instance=RequestContext(request))

def delmarker(request, marker_id):
    if request.user.is_authenticated():
        marker = Marker.objects.get(pk=marker_id)
        if marker:
            marker.delete()
    return HttpResponseRedirect(reverse('location:index'))