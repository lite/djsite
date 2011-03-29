from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from rankinghandler import GameHandler, GameRankHandler, ScoreHandler, AddScoreHandler
from accountshandler import LoginHandler, RegisterHandler, SchoolHandler, GradeHandler, ClassesHandler
from markerhandler import MarkerHandler, AddMarkerHandler, DelMarkerHandler
from contactshandler import MesgSendHandler
from lessonshandler import LessonsUpdHandler
from newshandler import ReportHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

#account
login_resource = CsrfExemptResource(LoginHandler)
register_resource = CsrfExemptResource(RegisterHandler)
school_resource = Resource(SchoolHandler)
grade_resource = Resource(GradeHandler)
classes_resource = Resource(ClassesHandler)

#news 
report_resource = Resource(ReportHandler)

# contacts
mesgsend_resource = CsrfExemptResource(MesgSendHandler)

# lessons
lessonsupd_resource = Resource(LessonsUpdHandler)

# location
marker_resource = Resource(MarkerHandler)
#addmarker_resource = CsrfExemptResource(AddMarkerHandler, **ad)
addmarker_resource = CsrfExemptResource(AddMarkerHandler)
delmarker_resource = CsrfExemptResource(DelMarkerHandler, **ad)

# ranking
game_resource = Resource(GameHandler)
gamerank_resource = Resource(GameRankHandler)
score_resource = Resource(ScoreHandler)
addscore_resource = CsrfExemptResource(AddScoreHandler, **ad)
# addscore_resource = Resource(ModelHandler)

urlpatterns = patterns('',
    # user
    url(r'^accounts/login/?$', login_resource),
    url(r'^accounts/register/?$', register_resource), 
    url(r'^accounts/profile/school/(?P<school_id>\d+)/?$', school_resource),
    url(r'^accounts/profile/grade/(?P<grade_id>\d+)/?$', grade_resource),
    url(r'^accounts/profile/classes/(?P<classes_id>\d+)/?$', classes_resource),
    
    # news 
    url(r'^news/?$', report_resource),
    
    #contacts
    url(r'^contacts/mesgsend/?$', mesgsend_resource),
    
    #lessons
    url(r'^lessons/update/(?P<local_tag>\d+)/?$', lessonsupd_resource),
    
    # location
    url(r'^location/?$', marker_resource),
    url(r'^location/addmarker/?$', addmarker_resource), 
    url(r'^location/delmarker/?$', delmarker_resource), 
    
    # ranking
    url(r'^ranking/?$', game_resource),
    url(r'^ranking/(?P<game_id>\d+)/?$', gamerank_resource),
    url(r'^ranking/score/(?P<score_id>\d+)/?$', score_resource), 
    url(r'^ranking/addscore/?$', addscore_resource),
)