from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class MyUserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "last_login",
        "date_joined",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name")}),
        (("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    ordering = ("email",)
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    readonly_fields = ("date_joined",)


admin.site.register(User, MyUserAdmin)
