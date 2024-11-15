"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """User Manager."""

    def create_user(self, email, password=None, **kwargs):
        """Create"""
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        # `using=self._db` is just in case you want to add multiple dbs.
        # which is rare; but keep it just in case.
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User."""
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
