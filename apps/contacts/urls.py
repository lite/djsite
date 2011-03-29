from django.conf.urls.defaults import *
import views as contacts_views

urlpatterns = patterns("",
    url('^$', contacts_views.index, name='index'),
)
