from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    fieldsets = (
        (None, {"fields": (
            "email",
            "password",
            "last_login",
        )}),
        ("Personal info", {"fields": (
            ("first_name", "last_name"),
         )}),
        ("Permissions", {"fields": (
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ("email", "first_name", "last_name", "is_superuser", "is_active", "last_login")
    list_filter = ("is_staff", "is_active")
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ["email"]
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

