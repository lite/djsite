from piston.handler import BaseHandler
from piston.utils import rc, throttle

from apps.location.models import Marker
from datetime import datetime
from csrfhandler import CsrfHandler 

class CsrfExemptBaseHandler(BaseHandler):
    """
    handles request that have had csrfmiddlewaretoken inserted 
    automatically by django's CsrfViewMiddleware
    """
    def flatten_dict(self, dct):
        if 'csrfmiddlewaretoken' in dct:
            # dct is a QueryDict and immutable
            dct = dct.copy()  
            del dct['csrfmiddlewaretoken']
        return super(CsrfBaseHandler, self).flatten_dict(dct)

# location
class MarkerHandler(BaseHandler):
    allowed_methods = ('GET', )
    model = Marker
    exclude = ()
    
    def read(self, request):
        markers = Marker.objects.all().order_by('-date')[:10]
        return {'markers': markers }

class AddMarkerHandler(CsrfHandler):
    allowed_methods = ('POST', )

    # @throttle(5, 10*60) # allow 5 times in 10 minutes
    def create(self, request):
        # Create/POST code goes here. 
        # if request.user.is_authenticated():
        if True:
            marker = Marker()
            marker.phone = request.POST.get("phone")
            marker.latitude = request.POST.get("latitude")
            marker.longitude = request.POST.get("longitude")
            s_date = request.POST.get("date")
            if s_date:
                marker.date = datetime.strptime(s_date, "%Y-%m-%d %H:%M:%S")
            else:
                marker.date = datetime.now()
            marker.save()
            return marker

class DelMarkerHandler(CsrfExemptBaseHandler):
    allowed_methods = ('POST', )

    # @throttle(5, 10*60) # allow 5 times in 10 minutes
    def create(self, request):
        # Create/POST code goes here. 
        if request.user.is_authenticated():
            markers = request.POST.getlist("id")
            for marker_id in markers:
                marker = Marker.objects.get(pk=marker_id)
                if marker:
                    marker.delete()
            return {"markers": markers}

    