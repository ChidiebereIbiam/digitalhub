from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User
from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["first_name", "last_name","email", "is_superuser"]
    search_fields = ["email", "username"]