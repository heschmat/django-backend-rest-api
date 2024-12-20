"""
Serializers for the User API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User Object."""

    class Meta:
        # Model & the required fields &
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """
        Create and return a user with encrypted password.
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update info & return back the update user object."""
        user = super().update(instance, validated_data)
        # Check if password is being modified, set the new password.
        # If `password` not being updated, it's not in the validated_data.
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, props):
        email = props.get('email')
        password = props.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unsable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        props['user'] = user
        return props
