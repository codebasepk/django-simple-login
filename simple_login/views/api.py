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

from rest_framework import status
from rest_framework.response import Response

from simple_login.serializers import (
    ActivationKeyRequestSerializer,
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
    StatusSerializer,
    ActivationValidationSerializer,
    LoginSerializer,
    RetrieveUpdateDestroyProfileValidationSerializer,
)
from simple_login.views.base import (
    BaseAPIView,
    ProfileBaseAPIView,
    AuthenticatedRequestBaseAPIView,
)
from simple_login.utils.otp import OTPHandler


class ActivationAPIView(ProfileBaseAPIView):
    validation_class = ActivationValidationSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.activate()
        return Response(
            data=self.get_user_profile_data_with_token(),
            status=status.HTTP_200_OK
        )


class ActivationKeyRequestAPIView(BaseAPIView):
    validation_class = ActivationKeyRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        otp_handler = OTPHandler(self.get_user())
        otp_handler.generate_and_send_account_activation_otps(commit=True)
        return Response(status=status.HTTP_200_OK)


class LoginAPIView(ProfileBaseAPIView):
    validation_class = LoginSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return Response(
            data=self.get_user_profile_data_with_token(),
            status=status.HTTP_200_OK
        )


class PasswordResetRequestAPIView(BaseAPIView):
    validation_class = PasswordResetRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.generate_and_send_password_reset_email_otp()
        return Response(status=status.HTTP_200_OK)


class PasswordChangeAPIView(BaseAPIView):
    validation_class = PasswordChangeSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.change_password(
            self.serializer.data.get('new_password')
        )
        return Response(status=status.HTTP_200_OK)


class StatusAPIView(BaseAPIView):
    validation_class = StatusSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return Response(status=status.HTTP_200_OK)


class RetrieveUpdateDestroyProfileAPIView(AuthenticatedRequestBaseAPIView):
    validation_class = RetrieveUpdateDestroyProfileValidationSerializer
    http_method_names = ['put', 'get', 'delete']

    def get(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.get_auth_user())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        self.get_auth_user().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, *args, **kwargs):
        super().put(*args, **kwargs)
        serializer = self.update_fields_with_request_data()
        self.ensure_password_hashed()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
