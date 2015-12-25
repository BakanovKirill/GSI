from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GsiAppConfig(AppConfig):
    name = 'gsi'
    verbose_name = _(u"Tiles")

    def ready(self):
        from gsi import signals
