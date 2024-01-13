from django.contrib import admin
from users.models import *
from django.contrib.auth.admin import UserAdmin
# from unfold.admin import ModelAdmin

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    search_fields = ["email__startswith", "username__startswith"]
    list_display = [
        "id",
        "code",
        "username",
        "email",
        # "is_staff",
        # "is_superuser",
    ]
    list_filter = ["is_staff", "is_superuser"]
    list_display_links = ["username", "email"]
    ordering = ["id"]
    filter_horizontal = []
    fieldsets = [
        (None, {"fields": ["username", "email", "password"]}),
        ("Permissions", {"fields": ["is_staff", "is_superuser"]}),
    ]



# @admin.register(CustomUser)
# class CustomUserAdminClass(ModelAdmin):
#     pass