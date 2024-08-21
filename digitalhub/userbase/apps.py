from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserbaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'digitalhub.userbase'
    verbose_name = _("userbase")