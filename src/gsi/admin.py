from cards.models import CardItem, OrderedCardItem
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from core.utils import make_run, upload_files
from .models import (HomeVariables, VariablesGroup, Tile, Area, YearGroup,
                     Year, CardSequence, RunBase, RunStep, Run,
                     Resolution, Log, TileType, Satellite, InputDataDirectory,
                     ListTestFiles)
from solo.admin import SingletonModelAdmin


class AreaAdmin(admin.ModelAdmin):
    filter_horizontal = ('tiles',)


class YearGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('years',)


class CardsInline(admin.TabularInline):
    model = CardSequence.cards.through
    fields = ('card_item', 'order')


# class CardSequenceAdmin(admin.ModelAdmin):
#     inlines = (CardsInline,)
#     exclude = ('cards',)


# admin.site.register(CardSequence, CardSequenceAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(HomeVariables, SingletonModelAdmin)
admin.site.register(VariablesGroup, admin.ModelAdmin)
admin.site.register(Year, admin.ModelAdmin)
admin.site.register(YearGroup, YearGroupAdmin)
admin.site.register(Tile, admin.ModelAdmin)


class RunBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date_created', 'date_modified',)
    readonly_fields = ('author',)
    actions = ('launch',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

    def launch(self, request, queryset):
        for run_base in queryset:
            result = make_run(run_base, request.user)
            print 'Run created: %s' % result['run'].id
            print 'Step created: %s' % result['step'].id
        self.message_user(request, "Selected runs are launched.")
    launch.short_description = "Launch selected"


class RunAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'state', 'run_date')


class RunStepAdmin(admin.ModelAdmin):
    list_display = ('card_item', 'parent_run', 'state', 'start_date',)


admin.site.register(RunBase, RunBaseAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(RunStep, RunStepAdmin)
admin.site.register(Resolution, admin.ModelAdmin)
admin.site.register(Log, admin.ModelAdmin)
admin.site.register(TileType, admin.ModelAdmin)
admin.site.register(Satellite, admin.ModelAdmin)


class InputDataDirectoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = ('updated_file_list',)

    def updated_file_list(self, request, queryset):
        for dir in queryset:
            pass
            result = upload_files(dir.name)
        #     print 'Run created: %s' % result['run'].id
        #     print 'Step created: %s' % result['step'].id
        self.message_user(request, "For selected folders updated file list.")
    updated_file_list.short_description = "Updated file list"


class ListTestFilesAdmin(admin.ModelAdmin):
    list_display = ('name', 'input_data_directory', 'size', 'date_modified',)
    readonly_fields = ('name', 'input_data_directory', 'size', 'date_modified',)


admin.site.register(InputDataDirectory, InputDataDirectoryAdmin)
admin.site.register(ListTestFiles, ListTestFilesAdmin)
