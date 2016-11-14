# -*- coding: utf-8 -*-
from django.contrib import admin

from wiki.models import Wiki


class WikiAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Wiki, WikiAdmin)
