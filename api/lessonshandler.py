from piston.handler import BaseHandler
from piston.utils import rc, throttle

from apps.lessons.models import Package, Lesson

import pdb

class LessonsUpdHandler(BaseHandler):
    allowed_methods = ('GET', )
    # model = Package
    # fields = (('tag', 'lessons'))
    model = Lesson
    fields = (('version', 'path', 'link', 'summary'))
    
    def read(self, request, local_tag):
        #pdb.set_trace()
        packages = Package.objects.all().filter(tag__gt=local_tag)
        for package in packages:
            package.lessons = Lesson.objects.all().filter(package__exact=package)
        return {'packages':packages}
        