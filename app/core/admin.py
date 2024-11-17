"""
Django Admin Panel Customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _  # future proofing

from core import models


class UserAdmin(BaseUserAdmin):
    """Define customized `UserAdmin` class for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('important dates'), {'fields': ('last_login',)})

    )

    readonly_fields = ['last_login']
    # Fields for add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'name',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),  # don't forget the `,` => TypeError: cannot unpack non-iterable NoneType object
    )


# Register our `User` model with the above `UserAdmin` customization.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
