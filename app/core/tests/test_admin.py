"""
Tests for the Django admin modifications.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminPanelTests(TestCase):
    """Tests for Django Admin Panel."""

    def setUp(self):
        """Create user & client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='Admin123'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user1@example.com',
            password='Whatever1',
            name='User1'
        )

    def test_users_list(self):
        """Test that Users are listen on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
