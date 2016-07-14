# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
# Simple Login
# Copyright (C) 2016 byteShaft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from rest_framework import (
    exceptions as drf_exceptions,
    serializers
)

from simple_login.exceptions import NotModified, Forbidden
from simple_login.models import BaseUser, KEY_DEFAULT_VALUE


class CustomBaseSerializer(serializers.Serializer):
    email = None

    def __init__(self, user_model, **kwargs):
        super().__init__(**kwargs)
        self.user_model = user_model
        if not self.user_model or not issubclass(self.user_model, BaseUser):
            msg = 'user_model must be an instance of ' \
                  'simple_login.models.BaseUser'
            raise serializers.ValidationError(msg)

    def validate(self, attrs):
        """A common call that's part of every request."""
        self.email = attrs.get('email')

    def raise_if_user_does_not_exist(self):
        try:
            return self.user_model.objects.get(email=self.email)
        except self.user_model.DoesNotExist:
            msg = 'User with email \'{}\' does not exist.'.format(self.email)
            raise drf_exceptions.NotFound(msg)

    def raise_if_user_already_activated(self):
        user = self.user_model.objects.get(email=self.email)
        if user.is_active:
            msg = 'User already activated.'
            raise NotModified(msg)

    def raise_if_user_not_activated(self):
        user = self.user_model.objects.get(email=self.email)
        if not user.is_active:
            msg = 'User not active.'
            raise Forbidden(msg)


class ActivationKeyRequestSerializer(CustomBaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        self.raise_if_user_already_activated()
        return attrs


class AccountActivationValidationSerializer(CustomBaseSerializer):
    email = serializers.EmailField(label='Email')
    activation_key = serializers.IntegerField(label='Activation key')

    def _raise_if_activation_key_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        key = user.account_activation_key
        if key == KEY_DEFAULT_VALUE or key != int(self.activation_key):
            msg = 'Invalid activation key.'
            raise serializers.ValidationError(msg)

    def validate(self, attrs):
        super().validate(attrs)
        self.activation_key = attrs.get('activation_key')
        self.raise_if_user_does_not_exist()
        self.raise_if_user_already_activated()
        self._raise_if_activation_key_invalid()
        return attrs


class LoginSerializer(CustomBaseSerializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(label='Password')

    def _raise_if_password_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        if not user.check_password(self.password):
            msg = 'Invalid password.'
            raise drf_exceptions.AuthenticationFailed(msg)

    def validate(self, attrs):
        super().validate(attrs)
        self.password = attrs.get('password')
        self.raise_if_user_does_not_exist()
        self.raise_if_user_not_activated()
        self._raise_if_password_invalid()
        return attrs


class PasswordResetRequestSerializer(CustomBaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        return attrs


class PasswordChangeSerializer(CustomBaseSerializer):
    email = serializers.EmailField(label='Email')
    password_reset_key = serializers.IntegerField(label='Password reset key')
    new_password = serializers.CharField(label='New password')

    def _raise_if_password_reset_key_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        key = user.password_reset_key
        if key == KEY_DEFAULT_VALUE or key != int(self.password_reset_key):
            msg = 'Invalid password reset key.'
            raise serializers.ValidationError(msg)

    def validate(self, attrs):
        super().validate(attrs)
        self.password_reset_key = attrs.get('password_reset_key')
        self.raise_if_user_does_not_exist()
        self._raise_if_password_reset_key_invalid()
        return attrs


class StatusSerializer(CustomBaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        self.raise_if_user_not_activated()
        return attrs


class RetrieveUpdateDestroyValidationSerializer(CustomBaseSerializer):
    email = serializers.CharField(label='Email', required=False)

    def validate(self, attrs):
        super().validate(attrs)
        if self.email:
            msg = 'Not allowed to change Email.'
            raise Forbidden(msg)

        return attrs
