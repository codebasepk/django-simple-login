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

from django.conf import settings
from rest_framework import (
    exceptions as drf_exceptions,
    serializers
)

from simple_login import KEY_DEFAULT_VALUE
from simple_login.serializers.base import BaseSerializer
from simple_login.exceptions import Forbidden

OTP_METHOD_EMAIL = 'email'
OTP_METHOD_SMS = 'sms'

try:
    OTP_METHODS = [method.lower() for method in settings.OTP_METHODS]
except AttributeError:
    OTP_METHODS = [OTP_METHOD_EMAIL]


class ActivationKeyRequestSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        self.raise_if_user_already_activated()
        self.raise_if_user_deactivated_by_admin()
        return attrs


class ActivationValidationSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')
    email_otp = serializers.IntegerField(
        label='Email OTP', required=OTP_METHOD_EMAIL in OTP_METHODS)
    sms_otp = serializers.IntegerField(
        label='SMS OTP', required=OTP_METHOD_SMS in OTP_METHODS)

    def _raise_if_email_otp_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        otp = user.account_activation_email_otp
        if otp == KEY_DEFAULT_VALUE or otp != int(self.email_otp):
            raise serializers.ValidationError('Invalid email OTP.')

    def _raise_if_sms_otp_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        otp = user.account_activation_sms_otp
        if otp == KEY_DEFAULT_VALUE or otp != int(self.sms_otp):
            raise serializers.ValidationError('Invalid sms OTP.')

    def validate(self, attrs):
        super().validate(attrs)
        self.email_otp = attrs.get('email_otp')
        self.sms_otp = attrs.get('sms_otp')
        self.raise_if_user_does_not_exist()
        self.raise_if_user_already_activated()
        self.raise_if_user_deactivated_by_admin()
        if OTP_METHOD_EMAIL in OTP_METHODS:
            self._raise_if_email_otp_invalid()
        if OTP_METHOD_SMS in OTP_METHODS:
            self._raise_if_sms_otp_invalid()
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
        self.raise_if_user_deactivated_by_admin()
        self._raise_if_password_invalid()
        return attrs


class PasswordResetRequestSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        self.raise_if_user_deactivated_by_admin()
        return attrs


class PasswordChangeSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')
    email_otp = serializers.IntegerField(label='Password reset email OTP')
    new_password = serializers.CharField(label='New password')

    def _raise_if_password_reset_email_otp_invalid(self):
        user = self.user_model.objects.get(email=self.email)
        key = user.password_reset_email_otp
        if key == KEY_DEFAULT_VALUE or key != int(self.email_otp):
            raise serializers.ValidationError('Invalid email OTP')

    def validate(self, attrs):
        super().validate(attrs)
        self.email_otp = attrs.get('email_otp')
        self.raise_if_user_does_not_exist()
        self.raise_if_user_deactivated_by_admin()
        self._raise_if_password_reset_email_otp_invalid()
        return attrs


class StatusSerializer(BaseSerializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        super().validate(attrs)
        self.raise_if_user_does_not_exist()
        self.raise_if_user_not_activated()
        self.raise_if_user_deactivated_by_admin()
        return attrs


class RetrieveUpdateDestroyProfileValidationSerializer(BaseSerializer):
    email = serializers.CharField(label='Email', required=False)

    def validate(self, attrs):
        super().validate(attrs)
        if self.email:
            raise Forbidden('Not allowed to change email.')
        return attrs
