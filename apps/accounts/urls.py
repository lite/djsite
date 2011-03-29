from django.conf.urls.defaults import *
import views as accounts_views

urlpatterns = patterns("",
    url(r'^register/$', accounts_views.register, name="register"),
    url(r'^login/$', accounts_views.login, name="login"),
    url(r'^logout/$', accounts_views.logout, name="logout"),
)
