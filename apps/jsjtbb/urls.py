from django.conf.urls.defaults import *

from apps.jsjtbb import settings as forum_settings
from apps.jsjtbb import views as forum_views
from apps.jsjtbb.feeds import LastPosts, LastTopics, LastPostsOnForum,\
     LastPostsOnCategory, LastPostsOnTopic

feeds = {
    'posts': LastPosts,
    'topics': LastTopics,
    'topic': LastPostsOnTopic,
    'forum': LastPostsOnForum,
    'category': LastPostsOnCategory,
}

urlpatterns = patterns('',

    # Forum
    url('^$', forum_views.index, name='index'),
    url('^(?P<forum_id>\d+)/$', forum_views.show_forum, name='forum'),
    url('^moderate/(?P<forum_id>\d+)/$', forum_views.moderate, name='moderate'),
    url('^search/$', forum_views.search, name='search'),
    url('^misc/$', forum_views.misc, name='misc'),

    # User
    url('^user/(?P<username>.*)/$', forum_views.user, name='forum_profile'),
    url('^users/$', forum_views.users, name='forum_users'),

    # Topic
    url('^topic/(?P<topic_id>\d+)/$', forum_views.show_topic, name='topic'),
    url('^(?P<forum_id>\d+)/topic/add/$', forum_views.add_post, {'topic_id': None}, name='add_topic'),
    url('^topic/(?P<topic_id>\d+)/delete_posts/$', forum_views.delete_posts, name='delete_posts'),
    url('^topic/move/$', forum_views.move_topic, name='move_topic'),
    url('^topic/(?P<topic_id>\d+)/stick_unstick/$', forum_views.stick_unstick_topic, name='stick_unstick_topic'),
    url('^topic/(?P<topic_id>\d+)/open_close/$', forum_views.open_close_topic, name='open_close_topic'),

    # Post
    url('^topic/(?P<topic_id>\d+)/post/add/$', forum_views.add_post,
        {'forum_id': None}, name='add_post'),
    url('^post/(?P<post_id>\d+)/$', forum_views.show_post, name='post'),
    url('^post/(?P<post_id>\d+)/edit/$', forum_views.edit_post, name='edit_post'),
    url('^post/(?P<post_id>\d+)/delete/$', forum_views.delete_post, name='delete_post'),
    # Post preview
    url(r'^preview/$', forum_views.post_preview, name='post_preview'),

    # Subscription
    url('^subscription/topic/(?P<topic_id>\d+)/delete/$', forum_views.delete_subscription, name='forum_delete_subscription'),
    url('^subscription/topic/(?P<topic_id>\d+)/add/$', forum_views.add_subscription, name='forum_add_subscription'),
    # Feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}, name='forum_feed'),
    
)


### EXTENSIONS ###

# LOFI Extension
if (forum_settings.LOFI_SUPPORT):
    urlpatterns += patterns('',
        url('^lofi/$', forum_views.index, {'full':False}, name='lofi_index'),
        url('^(?P<forum_id>\d+)/lofi/$', forum_views.show_forum, {'full':False}, name='lofi_forum'),
        url('^topic/(?P<topic_id>\d+)/lofi/$', forum_views.show_topic, {'full':False}, name='lofi_topic'),
    )

# REPUTATION Extension
if (forum_settings.REPUTATION_SUPPORT):
    urlpatterns += patterns('',
        url('^reputation/(?P<username>.*)/$', forum_views.reputation, name='reputation'),
    )

# ATTACHMENT Extension
if (forum_settings.ATTACHMENT_SUPPORT):
    urlpatterns += patterns('',
        url('^attachment/(?P<hash>\w+)/$', forum_views.show_attachment, name='forum_attachment'),
    )
