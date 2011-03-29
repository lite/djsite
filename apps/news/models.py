from django.db import models

from django.utils.translation import ugettext_lazy as _

class Report(models.Model):
    headline = models.CharField(_('Headline'), max_length=200, null=True, blank=True)
    content = models.TextField(_('Content'))
    reporter = models.CharField(max_length=50,)
    date = models.DateTimeField(null = True)

