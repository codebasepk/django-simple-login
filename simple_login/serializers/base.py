from rest_framework import (
    exceptions as drf_exceptions,
    serializers
)

from simple_login.exceptions import NotModified, Forbidden
from simple_login.models import BaseUser


class BaseSerializer(serializers.Serializer):
    email = None

    def __init__(self, user_model, **kwargs):
        super().__init__(**kwargs)
        if not issubclass(self.user_model, BaseUser):
            raise serializers.ValidationError(
                'user_model must be a subclass of simple_login.models.BaseUser'
            )
        self.user_model = user_model

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        """A common call that's part of every request."""
        self.email = attrs.get('email')

    def raise_if_user_does_not_exist(self):
        try:
            return self.user_model.objects.get(email=self.email)
        except self.user_model.DoesNotExist:
            raise drf_exceptions.NotFound(
                'User with email \'{}\' does not exist.'.format(self.email)
            )

    def raise_if_user_already_activated(self):
        user = self.user_model.objects.get(email=self.email)
        if user.is_active:
            raise NotModified('User already activated.')

    def raise_if_user_not_activated(self):
        user = self.user_model.objects.get(email=self.email)
        if not user.is_active:
            raise Forbidden('User not active.')