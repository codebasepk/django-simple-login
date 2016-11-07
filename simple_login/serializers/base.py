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
from simple_login.models import BaseUser

from simple_login import KEY_DEFAULT_VALUE


class BaseSerializer(serializers.Serializer):
    email = None

    def __init__(self, user_model, **kwargs):
        super().__init__(**kwargs)
        if not issubclass(user_model, BaseUser):
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
        if not user.is_active and \
                user.account_activation_email_otp != KEY_DEFAULT_VALUE:
            raise Forbidden('User not active.')

    def raise_if_user_deactivated_by_admin(self):
        user = self.user_model.objects.get(email=self.email)
        if not user.is_active and \
                user.account_activation_email_otp == KEY_DEFAULT_VALUE:
            raise Forbidden('User deactivated by admin.')
