from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class ModelAdmin(UserAdmin):
    model = CustomUser

    # fields that show up in admin list page
    list_display = ("email", "is_staff", "is_active", "date_of_birth")
    list_filter = ("is_staff", "is_active")

    # fields used when editing a user
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    # fields used in “create user” form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "date_of_birth", "profile_photo", "is_staff", "is_active"),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, ModelAdmin)
