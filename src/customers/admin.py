from django.contrib import admin

from customers.models import (Category, ShelfData, DataSet, CustomerAccess,
                            CustomerInfoPanel, CustomerPolygons, DataTerraserver,
                            DataPolygons, AttributesReport, LutFiles, TimeSeriesResults)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ShelfDataAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute_name', 'root_filename', 'units', 'scale', 'show_totals',)
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
    list_display = ('user', 'data_set', 'attribute_name', 'statistic',
                    'file_area_name', 'tif_path', 'png_path', 'url_png',
                    'legend_path', 'url_legend', 'order', 'is_show')
    search_fields = ['user', 'data_set', 'file_area_name']
    list_filter = ('user', 'data_set', 'file_area_name')
    
    
class CustomerPolygonsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'data_set', 'kml_name', 'kml_path', 'kml_url', 'text_kml')
    search_fields = ['user', 'name', 'data_set']
    list_filter = ('user', 'name', 'data_set')
    
    
class DataTerraserverAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'shapefile', 'shapefile_link', 'parameter', 'transaction_id')
    search_fields = ['user', 'shapefile']
    list_filter = ('user', 'shapefile')
    
    
class DataPolygonsAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_set', 'customer_polygons', 'attribute', 'statistic',
                    'value', 'units', 'total', 'total_area')
    search_fields = ['user', 'data_set', 'customer_polygons', 'attribute', 'statistic', 'units']
    list_filter = ('user', 'data_set', 'customer_polygons', 'attribute', 'statistic', 'units')
    
    
class AttributesReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_set', 'shelfdata', 'statistic')
    search_fields = ['user', 'data_set', 'shelfdata', 'statistic']
    list_filter = ('user', 'data_set', 'shelfdata', 'statistic')
    
    
class LutFilesAdmin(admin.ModelAdmin):
    list_display = ('name', 'lut_file', 'max_val', 'legend', 'units', 'val_scale')
    search_fields = ['name', 'lut_file', 'max_val']
    list_filter = ('name', 'lut_file', 'max_val')


class TimeSeriesResultsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'data_set', 'customer_polygons', 'result_year',
                    'stat_code', 'result_date', 'value_of_time_series')
    search_fields = ['user', 'name', 'data_set', 'customer_polygons', 'result_year',
                    'stat_code', 'result_date']
    list_filter = ('user', 'name', 'data_set', 'customer_polygons', 'result_year',
                    'stat_code', 'result_date', 'value_of_time_series')


admin.site.register(Category, CategoryAdmin)
admin.site.register(ShelfData, ShelfDataAdmin)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(CustomerAccess, CustomerAccessAdmin)
admin.site.register(CustomerInfoPanel, CustomerInfoPanelAdmin)
admin.site.register(CustomerPolygons, CustomerPolygonsAdmin)
admin.site.register(DataTerraserver, DataTerraserverAdmin)
admin.site.register(DataPolygons, DataPolygonsAdmin)
admin.site.register(AttributesReport, AttributesReportAdmin)
admin.site.register(LutFiles, LutFilesAdmin)
admin.site.register(TimeSeriesResults, TimeSeriesResultsAdmin)
