from piston.handler import BaseHandler
from piston.utils import rc, throttle

from apps.news.models import Report

class ReportHandler(BaseHandler):
    allowed_methods = ('GET', )
    model = Report
    
    def read(self, request):
        reports = Report.objects.all().order_by('-date')[:10]
        return {'reports':reports}
        
