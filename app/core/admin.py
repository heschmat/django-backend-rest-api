"""
Django Admin Panel Customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    """Define customized `UserAdmin` class for users."""
    ordering = ['id']
    list_display = ['email', 'name']


# Register our `User` model with the above `UserAdmin` customization.
admin.site.register(models.User, UserAdmin)
