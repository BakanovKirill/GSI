from django.contrib import admin

from customers.models import (Category, ShelfData, DataSet, CustomerAccess,
                            CustomerInfoPanel, CustomerPolygons, DataTerraserver)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ShelfDataAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute_name', 'root_filename', 'units', 'show_totals',)
    search_fields = ['category', 'attribute_name', 'root_filename',]
    list_filter = ('category', 'attribute_name', 'root_filename',)


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'results_directory', 'get_attribute_name', 'get_root_filename',)
    search_fields = ['name', 'description', 'get_attribute_name',]
    list_filter = ('name', 'description', 'shelf_data__attribute_name', 'shelf_data__root_filename',)

    def get_attribute_name(self, obj):
        if obj.shelf_data:
            return obj.shelf_data.attribute_name
        return

    def get_root_filename(self, obj):
        if obj.shelf_data:
            return obj.shelf_data.root_filename
        return

    get_attribute_name.short_description = 'Atribute Name'
    get_root_filename.short_description = 'Root Filename'


class CustomerAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_data_set',)
    search_fields = ['user',]
    list_filter = ('user',)
    filter_horizontal = ('data_set',)

    def get_data_set(self, obj):
        return "\n".join([p.name for p in obj.data_set.all()])

    get_data_set.short_description = 'DataSets'


class CustomerInfoPanelAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_set', 'attribute_name', 'statisctic', 'tif_path', 'png_path',)
    search_fields = ['user', 'data_set']
    list_filter = ('user', 'data_set')
    
    
class CustomerPolygonsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'kml_name', 'kml_path', 'url')
    search_fields = ['user', 'name']
    list_filter = ('user', 'name')
    
    
class DataTerraserverAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'shapefile', 'shapefile_link', 'parameter', 'transaction_id')
    search_fields = ['user', 'shapefile']
    list_filter = ('user', 'shapefile')


admin.site.register(Category, CategoryAdmin)
admin.site.register(ShelfData, ShelfDataAdmin)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(CustomerAccess, CustomerAccessAdmin)
admin.site.register(CustomerInfoPanel, CustomerInfoPanelAdmin)
admin.site.register(CustomerPolygons, CustomerPolygonsAdmin)
admin.site.register(DataTerraserver, DataTerraserverAdmin)
