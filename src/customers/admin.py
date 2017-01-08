from django.contrib import admin

from customers.models import (Category, InfoPanelMapping)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class InfoPanelMappingAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute_name', 'root_filename', 'units',)
    search_fields = ['category', 'attribute_name', 'root_filename',]
    list_filter = ('category', 'attribute_name', 'root_filename',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(InfoPanelMapping, InfoPanelMappingAdmin)
