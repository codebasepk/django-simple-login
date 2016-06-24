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
from rest_framework.views import APIView

from simple_login.serializers import (
    ActivationKeyRequestSerializer,
    AccountActivationSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
    StatusSerializer,
)
from simple_login.helpers import AccountHelpers


class CustomAPIView(APIView):
    user_model = None
    serializer = None

    @property
    def user_account(self):
        email = self.serializer.data.get('email')
        return AccountHelpers(self.user_model, email)


class RequestActivationKey(CustomAPIView):
    serializer_class = ActivationKeyRequestSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        self.serializer.is_valid(raise_exception=True)
        self.user_account.generate_and_send_account_activation_key()
        return Response(status=status.HTTP_200_OK)


class ActivateAccount(CustomAPIView):
    serializer_class = AccountActivationSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        self.serializer.is_valid(raise_exception=True)
        self.user_account.activate()
        return Response(status=status.HTTP_200_OK)


class Login(CustomAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        self.serializer.is_valid(raise_exception=True)
        auth_token = self.user_account.get_auth_token()
        return Response(
            data={'token': auth_token},
            status=status.HTTP_200_OK
        )


class RequestPasswordReset(CustomAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        self.serializer.is_valid(raise_exception=True)
        self.user_account.generate_and_send_password_reset_key()
        return Response(status=status.HTTP_200_OK)


class ChangePassword(CustomAPIView):
    serializer_class = PasswordChangeSerializer

    def change(self):
        new_password = self.serializer.data.get('new_password')
        self.user_account.change_password(new_password)

    def post(self, request, *args, **kwargs):
        self.serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        self.serializer.is_valid(raise_exception=True)
        self.change()
        return Response(status=status.HTTP_200_OK)


class AccountStatus(CustomAPIView):
    serializer_class = StatusSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)
