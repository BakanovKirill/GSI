# -*- coding: utf-8 -*-
from datetime import datetime
# import os
# from subprocess import call

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()
from django.db import IntegrityError

from gsi.settings import STATIC_ROOT, STATIC_DIR


class Wiki(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        verbose_name = _('Wiki')
        verbose_name_plural = _('Wiki')

    def __unicode__(self):
		return _(u"%s") % self.title
