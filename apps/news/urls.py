from django.conf.urls.defaults import *
import views as news_views

urlpatterns = patterns("",
    url('^$', news_views.index, name='index'),
    url('^addreport/$', news_views.addreport, name='addreport'),
)

