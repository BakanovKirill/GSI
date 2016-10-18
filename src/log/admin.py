from django.contrib import admin

from .models import Log, LogDebug


class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'element', 'element_id', 'message', 'at',)


class LogDebugAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date',)
    list_filter = ('name', 'create_date',)


admin.site.register(Log, LogAdmin)
admin.site.register(LogDebug, LogDebugAdmin)
