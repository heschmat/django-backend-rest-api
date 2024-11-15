"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_sucess(self):
        """Test creating a user with an email is success."""
        email = 'user@example.com'
        password = 'Random123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # .check_password() is provided by `BaseUserManager`
        self.assertTrue(user.checck_password(password))
