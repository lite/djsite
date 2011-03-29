from datetime import datetime
import os
import os.path
from markdown import Markdown

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.html import escape
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.hashcompat import sha_constructor

from apps.jsjtbb.markups import bbmarkup
from apps.jsjtbb.fields import AutoOneToOneField, ExtendedImageField, JSONField
from apps.jsjtbb.util import urlize, smiles
from apps.jsjtbb import settings as forum_settings

TZ_CHOICES = [(float(x[0]), x[1]) for x in (
    (-12, '-12'), (-11, '-11'), (-10, '-10'), (-9.5, '-09.5'), (-9, '-09'),
    (-8.5, '-08.5'), (-8, '-08 PST'), (-7, '-07 MST'), (-6, '-06 CST'),
    (-5, '-05 EST'), (-4, '-04 AST'), (-3.5, '-03.5'), (-3, '-03 ADT'),
    (-2, '-02'), (-1, '-01'), (0, '00 GMT'), (1, '+01 CET'), (2, '+02'),
    (3, '+03'), (3.5, '+03.5'), (4, '+04'), (4.5, '+04.5'), (5, '+05'),
    (5.5, '+05.5'), (6, '+06'), (6.5, '+06.5'), (7, '+07'), (8, '+08'),
    (9, '+09'), (9.5, '+09.5'), (10, '+10'), (10.5, '+10.5'), (11, '+11'),
    (11.5, '+11.5'), (12, '+12'), (13, '+13'), (14, '+14'),
)]

SIGN_CHOICES = (
    (1, 'PLUS'),
    (-1, 'MINUS'),
)

PRIVACY_CHOICES = (
    (0, _(u'Display your e-mail address.')),
    (1, _(u'Hide your e-mail address but allow form e-mail.')),
    (2, _(u'Hide your e-mail address and disallow form e-mail.')),
)

MARKUP_CHOICES = (
    ('bbcode', 'bbcode'),
    ('markdown', 'markdown'),
)

path = os.path.join(settings.MEDIA_ROOT, 'forum', 'themes')
THEME_CHOICES = [(theme, theme) for theme in os.listdir(path) 
                 if os.path.isdir(os.path.join(path, theme))]

class Category(models.Model):
    name = models.CharField(_('Name'), max_length=80)
    groups = models.ManyToManyField(Group,blank=True, null=True, verbose_name=_('Groups'), help_text=_('Only users from these groups can see this category'))
    position = models.IntegerField(_('Position'), blank=True, default=0)

    class Meta:
        ordering = ['position']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name

    def forum_count(self):
        return self.forums.all().count()

    @property
    def topics(self):
        return Topic.objects.filter(forum__category=self).select_related()

    @property
    def posts(self):
        return Post.objects.filter(topic__forum__category=self).select_related()

    def has_access(self, user):
        if self.groups.count() > 0:
            if user.is_authenticated(): 
                try:
                    self.groups.get(user__pk=user.id)
                except Group.DoesNotExist:
                    return False
            else:
                return False
        return True


class Forum(models.Model):
    category = models.ForeignKey(Category, related_name='forums', verbose_name=_('Category'))
    name = models.CharField(_('Name'), max_length=80)
    position = models.IntegerField(_('Position'), blank=True, default=0)
    description = models.TextField(_('Description'), blank=True, default='')
    moderators = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Moderators'))
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    topic_count = models.IntegerField(_('Topic count'), blank=True, default=0)
    last_post = models.ForeignKey('Post', related_name='last_forum_post', blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jsjtbb:forum', [self.id])

    @property
    def posts(self):
        return Post.objects.filter(topic__forum=self).select_related()


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics', verbose_name=_('Forum'))
    name = models.CharField(_('Subject'), max_length=255)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), null=True)
    user = models.ForeignKey(User, verbose_name=_('User'))
    views = models.IntegerField(_('Views count'), blank=True, default=0)
    sticky = models.BooleanField(_('Sticky'), blank=True, default=False)
    closed = models.BooleanField(_('Closed'), blank=True, default=False)
    subscribers = models.ManyToManyField(User, related_name='subscriptions', verbose_name=_('Subscribers'), blank=True)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    last_post = models.ForeignKey('Post', related_name='last_topic_post', blank=True, null=True)

    class Meta:
        ordering = ['-updated']
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __unicode__(self):
        return self.name

    @property
    def head(self):
        try:
            return self.posts.select_related().order_by('created')[0]
        except IndexError:
            return None

    @property
    def reply_count(self):
        return self.post_count - 1

    @models.permalink
    def get_absolute_url(self):
        return ('jsjtbb:topic', [self.id])

    def update_read(self, user):
        tracking = user.posttracking
        #if last_port is None - don't check topics
        if self.last_post is None:
            return
        #if last_read > last_read - don't check topics
        if tracking.last_read and (tracking.last_read > self.last_post.created):
            return
        if isinstance(tracking.topics, dict):
            #clear topics if len > 5Kb and set last_read to current time
            if len(tracking.topics) > 5120:
                tracking.topics = None
                tracking.last_read = datetime.now()
                tracking.save()
            #update topics if exist new post or does't exist in dict
            if self.last_post.id > tracking.topics.get(str(self.id), 0):
                tracking.topics[str(self.id)] = self.last_post.id
                tracking.save()
        else:
            #initialize topic tracking dict
            tracking.topics = {self.id: self.last_post.id}
            tracking.save()


class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts', verbose_name=_('Topic'))
    user = models.ForeignKey(User, related_name='posts', verbose_name=_('User'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)
    updated_by = models.ForeignKey(User, verbose_name=_('Updated by'), blank=True, null=True)
    markup = models.CharField(_('Markup'), max_length=15, default=forum_settings.DEFAULT_MARKUP, choices=MARKUP_CHOICES)
    body = models.TextField(_('Message'))
    body_html = models.TextField(_('HTML version'))
    user_ip = models.IPAddressField(_('User IP'), blank=True, null=True)


    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def save(self, *args, **kwargs):
        if self.markup == 'bbcode':
            self.body_html = bbmarkup.bbcode(self.body)
        elif self.markup == 'markdown' and MARKDOWN_AVAILABLE:
            self.body_html = unicode(Markdown(self.body, safe_mode='escape'))
            #self.body_html = markdown(self.body, 'safe')
        else:
            raise Exception('Invalid markup property: %s' % self.markup)
        self.body_html = urlize(self.body_html)
        if forum_settings.SMILES_SUPPORT:
            self.body_html = smiles(self.body_html)
        super(Post, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self_id = self.id
        head_post_id = self.topic.posts.order_by('created')[0].id
        forum = self.topic.forum
        topic = self.topic
        profile = self.user.forum_profile
        self.last_topic_post.clear()
        self.last_forum_post.clear()
        super(Post, self).delete(*args, **kwargs)
        #if post was last in topic - remove topic
        if self_id == head_post_id:
            topic.delete()
        else:
            try:
                topic.last_post = Post.objects.filter(topic=topic).latest()
            except Post.DoesNotExist:
                topic.last_post = None
            topic.post_count = Post.objects.filter(topic=topic).count()
            topic.save()
        try:
            forum.last_post = Post.objects.filter(topic__forum=forum).latest()
        except Post.DoesNotExist:
            forum.last_post = None
        #TODO: for speedup - save/update only changed fields
        forum.post_count = Post.objects.filter(topic__forum=forum).count()
        forum.topic_count = Topic.objects.filter(forum=forum).count()
        forum.save()
        profile.post_count = Post.objects.filter(user=self.user).count()
        profile.save()

    @models.permalink
    def get_absolute_url(self):
        return ('jsjtbb:post', [self.id])

    def summary(self):
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or '' 
        return self.body[:LIMIT] + tail

    __unicode__ = summary


class Reputation(models.Model):
    from_user = models.ForeignKey(User, related_name='reputations_from', verbose_name=_('From'))
    to_user = models.ForeignKey(User, related_name='reputations_to', verbose_name=_('To'))
    post = models.ForeignKey(Post, related_name='post', verbose_name=_('Post'))
    time = models.DateTimeField(_('Time'), auto_now_add=True)
    sign = models.IntegerField(_('Sign'), choices=SIGN_CHOICES, default=0)
    reason = models.TextField(_('Reason'), max_length=1000)

    class Meta:
        verbose_name = _('Reputation')
        verbose_name_plural = _('Reputations')
        unique_together = (('from_user', 'post'),)

    def __unicode__(self):
        return u'T[%d], FU[%d], TU[%d]: %s' % (self.post.id, self.from_user.id, self.to_user.id, unicode(self.time))


class Profile(models.Model):
    user = AutoOneToOneField(User, related_name='forum_profile', verbose_name=_('User'))
    status = models.CharField(_('Status'), max_length=30, blank=True)
    site = models.URLField(_('Site'), verify_exists=False, blank=True)
    jabber = models.CharField(_('Jabber'), max_length=80, blank=True)
    icq = models.CharField(_('ICQ'), max_length=12, blank=True)
    msn = models.CharField(_('MSN'), max_length=80, blank=True)
    aim = models.CharField(_('AIM'), max_length=80, blank=True)
    yahoo = models.CharField(_('Yahoo'), max_length=80, blank=True)
    location = models.CharField(_('Location'), max_length=30, blank=True)
    signature = models.TextField(_('Signature'), blank=True, default='', max_length=forum_settings.SIGNATURE_MAX_LENGTH)
    time_zone = models.FloatField(_('Time zone'), choices=TZ_CHOICES, default=float(forum_settings.DEFAULT_TIME_ZONE))
    language = models.CharField(_('Language'), max_length=5, default='', choices=settings.LANGUAGES)
    avatar = ExtendedImageField(_('Avatar'), blank=True, default='', upload_to=forum_settings.AVATARS_UPLOAD_TO, width=forum_settings.AVATAR_WIDTH, height=forum_settings.AVATAR_HEIGHT)
    theme = models.CharField(_('Theme'), choices=THEME_CHOICES, max_length=80, default='default')
    show_avatar = models.BooleanField(_('Show avatar'), blank=True, default=True)
    show_signatures = models.BooleanField(_('Show signatures'), blank=True, default=True)
    privacy_permission = models.IntegerField(_('Privacy permission'), choices=PRIVACY_CHOICES, default=1)
    markup = models.CharField(_('Default markup'), max_length=15, default=forum_settings.DEFAULT_MARKUP, choices=MARKUP_CHOICES)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def last_post(self):
        posts = Post.objects.filter(user=self.user).order_by('-created')
        if posts:
            return posts[0].created
        else:
            return  None

    def reply_count_minus(self):
        return Reputation.objects.filter(to_user=self.user, sign=-1).count()

    def reply_count_plus(self):
        return Reputation.objects.filter(to_user=self.user, sign=1).count()


class PostTracking(models.Model):
    """
    Model for tracking read/unread posts.
    In topics stored ids of topics and last_posts as dict.
    """

    user = AutoOneToOneField(User)
    topics = JSONField(null=True)
    last_read = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _('Post tracking')
        verbose_name_plural = _('Post tracking')

    def __unicode__(self):
        return self.user.username


class Report(models.Model):
    reported_by = models.ForeignKey(User, related_name='reported_by', verbose_name=_('Reported by'))
    post = models.ForeignKey(Post, verbose_name=_('Post'))
    zapped = models.BooleanField(_('Zapped'), blank=True, default=False)
    zapped_by = models.ForeignKey(User, related_name='zapped_by', blank=True, null=True,  verbose_name=_('Zapped by'))
    created = models.DateTimeField(_('Created'), blank=True)
    reason = models.TextField(_('Reason'), blank=True, default='', max_length='1000')

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')

    def __unicode__(self):
        return u'%s %s' % (self.reported_by ,self.zapped)


class PrivateMessage(models.Model):
    dst_user = models.ForeignKey(User, verbose_name=_('Recipient'), related_name='dst_users')
    src_user = models.ForeignKey(User, verbose_name=_('Author'), related_name='src_users')
    read = models.BooleanField(_('Read'), blank=True, default=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    markup = models.CharField(_('Markup'), max_length=15, default=forum_settings.DEFAULT_MARKUP, choices=MARKUP_CHOICES)
    subject = models.CharField(_('Subject'), max_length=255)
    body = models.TextField(_('Message'))
    body_html = models.TextField(_('HTML version'))
    body_text = models.TextField(_('Text version'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('Private message')
        verbose_name_plural = _('Private messages')

    def __unicode__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if self.markup == 'bbcode':
            self.body_html = bbmarkup.bbcode(self.body)
        elif self.markup == 'markdown':
            self.body_html = unicode(Markdown(self.body, safe_mode='escape'))
            #self.body_html = markdown(self.body, 'safe')
        else:
            raise Exception('Invalid markup property: %s' % self.markup)
        self.body_html = urlize(self.body_html)
        if forum_settings.SMILES_SUPPORT:
            self.body_html = smiles(self.body_html)
        super(PrivateMessage, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return  ('jsjtbb:forum_show_pm', [self.id])

    # TODO: summary and part of the save method is the same as in the Post model
    # move to common functions
    def summary(self):
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or '' 
        return self.body[:LIMIT] + tail


class Ban(models.Model):
    user = models.OneToOneField(User, verbose_name=_('Banned user'), related_name='ban_users')
    ban_start = models.DateTimeField(_('Ban start'), default=datetime.now)
    ban_end = models.DateTimeField(_('Ban end'), blank=True, null=True)
    reason = models.TextField(_('Reason'))

    class Meta:
        verbose_name = _('Ban')
        verbose_name_plural = _('Bans')

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.user.is_active = False
        self.user.save()
        super(Ban, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.is_active = True
        self.user.save()
        super(Ban, self).delete(*args, **kwargs)


class Attachment(models.Model):
    post = models.ForeignKey(Post, verbose_name=_('Post'), related_name='attachments')
    size = models.IntegerField(_('Size'))
    content_type = models.CharField(_('Content type'), max_length=255)
    path = models.CharField(_('Path'), max_length=255)
    name = models.TextField(_('Name'))
    hash = models.CharField(_('Hash'), max_length=40, blank=True, default='', db_index=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Attachment, self).save(*args, **kwargs)
        if not self.hash:
            self.hash = sha_constructor(str(self.id) + settings.SECRET_KEY).hexdigest()
        super(Attachment, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('jsjtbb:forum_attachment', [self.hash])

    def get_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, forum_settings.ATTACHMENT_UPLOAD_TO,
                            self.path)
