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
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized (when created)."""
        sample_emails = (
            ('user1@EXAMPLE.com', 'user1@example.com'),
            ('User1@Example.COM', 'user1@example.com'),
            ('user1@Example.Com', 'user1@example.com')
        )
