from optparse import make_option
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from apps.jsjtbb.models import Ban


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, 
                    help=u'Unban all users'),
        make_option('--in-time', action='store_true', dest='in-time', default=False, 
                    help=u'Unban users in time'),
    )
    help = u'Unban users'
    
    def handle(self, *args, **options):
        if options['all']:
            bans = Ban.objects.all()
            user_ids = bans.values_list('user', flat=True)
            users = User.objects.filter(id__in=user_ids).update(is_active=True)
            bans.delete()
        elif options['in-time']:
            bans = Ban.objects.filter(ban_end__lte=datetime.now())
            user_ids = bans.values_list('user', flat=True)
            users = User.objects.filter(id__in=user_ids).update(is_active=True)
            bans.delete()
        else:
            print 'Invalid options'
