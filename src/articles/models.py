# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __unicode__(self):
		return _(u"%s") % self.title


class ArticleNonUpload(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextField()

    class Meta:
        verbose_name = _('Article Non Upload')
        verbose_name_plural = _('Articles Non Upload')

    def __unicode__(self):
		return _(u"%s") % self.title
