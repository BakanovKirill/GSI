from cards.models import CardItem, OrderedCardItem
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from .models import HomeVariables, VariablesGroup, Tile, Area, YearGroup, Year, CardSequence, RunBase, RunStep, Run, \
    Resolution, Log, TileType
from solo.admin import SingletonModelAdmin


class AreaAdmin(admin.ModelAdmin):
    filter_horizontal = ('tiles',)


class YearGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('years',)


class CardsInline(admin.TabularInline):
    model = CardSequence.cards.through

    fields = ('card_item', 'order')


class CardSequenceAdmin(admin.ModelAdmin):
    inlines = (CardsInline,)
    exclude = ('cards',)


admin.site.register(CardSequence, CardSequenceAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(HomeVariables, SingletonModelAdmin)
admin.site.register(VariablesGroup, admin.ModelAdmin)
admin.site.register(Year, admin.ModelAdmin)
admin.site.register(YearGroup, YearGroupAdmin)
admin.site.register(Tile, admin.ModelAdmin)


class RunBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date_created', 'date_modified')
    # exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(RunBase, RunBaseAdmin)
admin.site.register(Run, admin.ModelAdmin)
admin.site.register(RunStep, admin.ModelAdmin)
admin.site.register(Resolution, admin.ModelAdmin)
admin.site.register(Log, admin.ModelAdmin)
admin.site.register(TileType, admin.ModelAdmin)
