from django.conf.urls.defaults import *
from apps.ranking import views as ranking_views

urlpatterns = patterns("",
    url('^$', ranking_views.index, name='index'),
    url('^addscore/(?P<game_id>\d+)/$', ranking_views.addscore, name='addscore'),
)

