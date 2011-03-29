from piston.handler import BaseHandler
from piston.utils import rc, throttle

class CsrfHandler(BaseHandler):
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