from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.


class UserAdmin(AuthUserAdmin):
    model = User
    search_fields = ("email", "type")
    list_filter = ("email", "is_active", "is_staff", "is_superuser")
    list_display = ("email", "is_active", "is_staff", "id")
    fieldsets = (
        (None, {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "is_active",
                    "is_staff",

                ),
            },
        ),
    )

    readonly_fields = ("last_login",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
