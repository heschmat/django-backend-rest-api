"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# user: the `app_name` in the `user.urls`
# add_user: the `name` in the `path` added to urlpatterns in `user.urls`
CREATE_USER_URL = reverse('user:add_user')
TOKEN_URL = reverse('user:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserAPITestsPublic(TestCase):
    """Tests public features, i.e., no auth required."""

    def setUp(self):
        self.client = APIClient()
        self.default_payload = {
            'email': 'user1@example.com',
            'password': 'Whatever123',
            'name': 'Skye Q'
        }

    def _get_payload(self, **overrides):
        """Helper method to generate a payload with optional overrides."""
        payload = self.default_payload.copy()
        payload.update(overrides)
        return payload

    def test_create_user_ok(self):
        """Tests new user creation is successful."""
        payload = self._get_payload()
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Validate the above user is indeed created.
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        # Passwords should not be send back.
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Tests that creating a user with an existing email returns an error."""
        payload = self._get_payload()
        _ = create_user(**payload)  # Create a user with the given info

        # Try to create a user with the same email, which should return an error
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Passwords cannot be less than 8 char long."""
        # Create a user with short password:
        payload = self._get_payload(password='123')
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Make sure that the try to create a user has failed.
        # i.e, when a user gives a short password upon creation.
        user_created = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_created)

    def test_create_token_for_user(self):
        """Test for valid credentials token is generated."""
        user_info = self._get_payload()
        _ = create_user(**user_info)

        payload = {k: v for k, v in user_info.items() if k != 'name'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """"""
        payload = self._get_payload()
        _ = create_user(**payload)

        payload['password'] = ['wrong_pass']
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Password is mandatory when loggingin."""
        payload = {'email': 'user@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
