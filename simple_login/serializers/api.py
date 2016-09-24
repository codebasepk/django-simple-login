from rest_framework import (
    exceptions as drf_exceptions,
    serializers
)

from simple_login.serializers.base import BaseSerializer
from simple_login.exceptions import Forbidden
from simple_login.models import KEY_DEFAULT_VALUE


class ActivationKeyRequestSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        self.raise_if_user_already_activated()
        return attrs


class ActivationValidationSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')
    activation_key = serializers.IntegerField(label='Activation key')

    def _raise_if_activation_key_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        key = user.account_activation_key
        if key == KEY_DEFAULT_VALUE or key != int(self.activation_key):
            raise serializers.ValidationError('Invalid activation key.')

    def validate(self, attrs):
        super().validate(attrs)
        self.activation_key = attrs.get('activation_key')
        self.raise_if_user_does_not_exist()
        self.raise_if_user_already_activated()
        self._raise_if_activation_key_invalid()
        return attrs


class LoginSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(label='Password')

    def _raise_if_password_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        if not user.check_password(self.password):
            raise drf_exceptions.AuthenticationFailed('Invalid password.')

    def validate(self, attrs):
        super().validate(attrs)
        self.password = attrs.get('password')
        self.raise_if_user_does_not_exist()
        self.raise_if_user_not_activated()
        self._raise_if_password_invalid()
        return attrs


class PasswordResetRequestSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        return attrs


class PasswordChangeSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')
    password_reset_key = serializers.IntegerField(label='Password reset key')
    new_password = serializers.CharField(label='New password')

    def _raise_if_password_reset_key_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        key = user.password_reset_key
        if key == KEY_DEFAULT_VALUE or key != int(self.password_reset_key):
            raise serializers.ValidationError('Invalid password reset key.')

    def validate(self, attrs):
        super().validate(attrs)
        self.password_reset_key = attrs.get('password_reset_key')
        self.raise_if_user_does_not_exist()
        self._raise_if_password_reset_key_invalid()
        return attrs


class StatusSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        self.raise_if_user_not_activated()
        return attrs


class RetrieveUpdateDestroyProfileValidationSerializer(BaseSerializer):
    email = serializers.CharField(label='Email', required=False)

    def validate(self, attrs):
        super().validate(attrs)
        if self.email:
            raise Forbidden('Not allowed to change email.')
        return attrs
