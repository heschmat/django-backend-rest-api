"""
URL mappings for the User API.
"""

from django.urls import path

from user import views

app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='add_user'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
