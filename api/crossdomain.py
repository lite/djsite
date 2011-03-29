from django import http
import logging as _logging
from django.conf import settings as _settings

logger = _logging.getLogger(__name__)
logger.setLevel(getattr(_settings, 'LOG_LEVEL', _logging.DEBUG))

try:
    import settings 
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE', 'HEAD']


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         

        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE, HEAD
    """
    def process_request(self, request):
        logger.debug("Processing request")
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            if 'HTTP_ORIGIN' in request.META:
                response['Access-Control-Allow-Origin']  = request.META['HTTP_ORIGIN']
            else:
                response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
                
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            response['Access-Control-Allow-Credentials'] = 'true'

            return response

        return None

    def process_response(self, request, response):
        logger.debug("Processing response")
        if 'HTTP_ORIGIN' in request.META:
            response['Access-Control-Allow-Origin']  = request.META['HTTP_ORIGIN']
        else:
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS        
        
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Credentials'] = 'true'

        return response
