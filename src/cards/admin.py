from django.contrib.contenttypes.models import ContentType

from django.contrib import admin
from django import forms
from django.db.models import Q
from django.utils.translation import \
    ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()
from .models import (RFScore, QRF, Collate, YearFilter,
                     Remap, PreProc, MergeCSV, RFTrain,
                     CardItem, OrderedCardItem, RandomForest)
from gsi.models import ListTestFiles

admin.site.register(QRF, admin.ModelAdmin)
admin.site.register(RFScore, admin.ModelAdmin)
admin.site.register(Remap, admin.ModelAdmin)
admin.site.register(YearFilter, admin.ModelAdmin)
admin.site.register(PreProc, admin.ModelAdmin)
admin.site.register(MergeCSV, admin.ModelAdmin)
admin.site.register(RFTrain, admin.ModelAdmin)
admin.site.register(RandomForest, admin.ModelAdmin)
admin.site.register(OrderedCardItem, admin.ModelAdmin)

admin.site.register(ContentType)


class CollateAdminForm(forms.ModelForm):
    class Meta:
        model = Collate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CollateAdminForm, self).__init__(*args, **kwargs)
        if 'input_data_directory' in self.initial:
            self.fields['input_files'].queryset = ListTestFiles.objects.filter(
                    Q(input_data_directory=self.initial['input_data_directory']))
        else:
            pass


class CollateAdmin(admin.ModelAdmin):
    form = CollateAdminForm
    filter_horizontal = ('input_files',)


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
admin.site.register(Collate, CollateAdmin)
