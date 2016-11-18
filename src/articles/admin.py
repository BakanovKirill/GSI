# -*- coding: utf-8 -*-
from django.contrib import admin

from articles.models import Article, ArticleNonUpload


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)

class ArticleNonUploadAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleNonUpload, ArticleNonUploadAdmin)
