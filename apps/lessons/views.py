from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from models import Package, Lesson

def index(request):
    packages = Package.objects.all().order_by('-tag')[:10]
    for package in packages:
        package.lessons = Lesson.objects.all().filter(package__exact=package)
    return render_to_response('lessons/index.html', {'packages':packages}, context_instance=RequestContext(request))
