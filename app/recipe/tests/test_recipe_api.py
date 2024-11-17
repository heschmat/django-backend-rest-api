"""
Test for recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def get_detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **kwargs):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'A Delicious Recipe',
        'time_minutes': 10,
        'price': Decimal('9.99'),
        'description': 'You can make it!',
        'link': 'https://www.google.com/'
    }
    defaults.update(kwargs)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class RecipeAPITestsPublic(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authorized users can call only."""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class RecipeAPITestsAuthenticated(TestCase):
    """Test authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user1@gmail.com', 'Whatever123')
        self.client.force_authenticate(self.user)

    def test_retrive_recipes_ok(self):
        """Test retrieving user's recipe list."""
        # Create a couple of sample recipe for the user.
        for i in range(3):
            recipe_title = f'Recipe {i}'
            _ = create_recipe(self.user, title=recipe_title)
        # Make a GET request to get the list of recipes.
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test user have no access to other users' recipe list."""
        user2 = get_user_model().objects.create_user('user2@example.com', 'NotUser1')
        _ = create_recipe(user=user2)

        _ = create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # If user can see other recipes the following won't match.
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test user get's appropriate recipe detail."""
        recipe = create_recipe(user=self.user)

        url = get_detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
