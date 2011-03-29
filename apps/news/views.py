from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.core.urlresolvers import reverse

from models import Report
from forms import ReportForm

from datetime import datetime

def index(request):
    reports = Report.objects.all().order_by('-date')[:10]
    return render_to_response('news/index.html', {'reports':reports}, context_instance=RequestContext(request))
   
def addreport(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = Report() 
            report.headline = form.cleaned_data.get("headline")
            report.content = form.cleaned_data.get("content")
            report.reporter = request.user.username
            report.date = datetime.now()
            report.save()
            return HttpResponseRedirect(reverse('news:index'))
    else:
        form = ReportForm()

    return render_to_response('news/addreport.html', {'form':form}, context_instance=RequestContext(request))
  