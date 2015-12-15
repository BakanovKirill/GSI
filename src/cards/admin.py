from django.contrib.contenttypes.models import ContentType

from django.contrib import admin
from django.utils.translation import \
    ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()
from .models import RFScore, QRF, Collate, YearFilter, Remap, PreProc, MergeCSV, RFTrain, CardItem, OrderedCardItem

admin.site.register(QRF, admin.ModelAdmin)
admin.site.register(RFScore, admin.ModelAdmin)
admin.site.register(Remap, admin.ModelAdmin)
admin.site.register(Collate, admin.ModelAdmin)
admin.site.register(YearFilter, admin.ModelAdmin)
admin.site.register(PreProc, admin.ModelAdmin)
admin.site.register(MergeCSV, admin.ModelAdmin)
admin.site.register(RFTrain, admin.ModelAdmin)
admin.site.register(OrderedCardItem, admin.ModelAdmin)

admin.site.register(ContentType)


class CardItemAdmin(admin.ModelAdmin):
    fieldsets = (

        (_('Card'), {
            # 'classes': ('grp-collapse grp-open',),
            'fields': ('content_type', 'object_id', 'order')
        }),
    )

    # autocomplete_lookup_fields = {
    #     'contenttypes.models': [['content_type', 'object_id']],
    # }

    list_display = ('name', 'content_type')

    def name(self, instance):
        return u"{0}".format(instance.content_object)


admin.site.register(CardItem, CardItemAdmin)
