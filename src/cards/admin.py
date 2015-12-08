from django.contrib import admin
from .models import RFScore, QRF, Collate, YearFilter, Remap

admin.site.register(QRF, admin.ModelAdmin)
admin.site.register(RFScore, admin.ModelAdmin)
admin.site.register(Remap, admin.ModelAdmin)
admin.site.register(Collate, admin.ModelAdmin)
admin.site.register(YearFilter, admin.ModelAdmin)