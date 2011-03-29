from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

from sitemap import SitemapForum, SitemapTopic

sitemaps = {
    'forum': SitemapForum,
    'topic': SitemapTopic,
}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    #home
    (r'^$', 'apps.views.index'),
    #news
    (r'^news/', include('apps.news.urls', namespace='news')),
    #lessons
    (r'^lessons/', 'apps.lessons.views.index'),
    #contacts
    (r'^contacts/', include('apps.contacts.urls', namespace='contacts')),
    #location
    (r'^location/', include('apps.location.urls', namespace='location')),
    #rank
    (r'^ranking/', include('apps.ranking.urls', namespace='ranking')),
    # Sitemap
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    # Apps
    #(r'^forum/account/', include(authopenid_urlpatterns)),
    # (r'^accounts/', include('registration.urls')),
    (r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
    (r'^forum/', include('apps.jsjtbb.urls', namespace='jsjtbb')),
    #messages
    (r'^messages/', include('messages.urls')),
    #api
    (r'^api/', include('api.urls')),
)

from django.conf import settings

#if settings.DEBUG:
if True:
     urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

