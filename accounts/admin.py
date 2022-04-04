from django.contrib import admin

from accounts.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "country", "is_superuser", "is_active")
    search_fields = ("email", "is_active", "country")


admin.site.register(CustomUser, CustomUserAdmin)
