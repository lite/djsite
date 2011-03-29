from django.conf.urls.defaults import *
import views as location_views

urlpatterns = patterns("",
    url('^$', location_views.index, name='index'),
    url('^marker/(?P<marker_id>\d+)/$', location_views.showmarker, name='showmarker'),
    url('^addmarker/$', location_views.addmarker, name='addmarker'),
    url('^delmarker/(?P<marker_id>\d+)/$', location_views.delmarker, name='delmarker'),
)

