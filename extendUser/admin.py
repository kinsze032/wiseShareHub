from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {"fields": (
            "email",
            "password",
            "last_login",
        )}),
        ("Informacje dodatkowe", {"fields": (
            ("first_name", "last_name"),
         )}),
        ("Permissions", {"fields": (
            "is_superuser",
            "is_staff",
            "is_active",
        )}),
    )
    list_display = ("email", "first_name", "last_name", "is_superuser", "is_active", "last_login")
    list_filter = ("is_staff", "is_active")
    search_fields = ["email"]
    ordering = ["email"]


admin.site.register(User, UserAdmin)