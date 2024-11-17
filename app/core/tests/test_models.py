"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from decimal import Decimal

from core import models


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
        # Basically, username as is; the rest all lowercase.
        sample_emails = (
            ('user1@EXAMPLE.com', 'user1@example.com'),
            ('User2@Example.COM', 'User2@example.com'),
            ('USER3@EXAMPLE.COM', 'USER3@example.com'),
            ('user4@Example.Com', 'user4@example.com')
        )

        for email, expected_format in sample_emails:
            user = get_user_model().objects.create_user(email, 'Whatever123')
            self.assertEqual(user.email, expected_format)

    def test_new_user_withouth_email_fails(self):
        """Test creating a user w/o email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'Whatever123')

    def test_create_superuser(self):
        """Test."""
        user = get_user_model().objects.create_superuser(
            'admin@example.com',
            'Whatever123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe_ok(self):
        """Test creating a recipe is success."""
        payload = {'email': 'user@example.com', 'password': 'Whatever123'}
        user = get_user_model().objects.create_user(**payload)
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe Title',
            time_minutes=5,
            price=Decimal('5.99'),
            description='Very easy recipe.',
        )
        self.assertEqual(str(recipe), recipe.title)
