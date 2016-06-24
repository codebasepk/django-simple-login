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
from rest_framework.authtoken.models import Token

from simple_login.serializers import (
    ActivationKeyRequestSerializer,
    AccountActivationSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
    StatusSerializer,
)
from simple_login.helpers import (
    generate_random_key,
    send_account_activation_email,
    send_password_reset_email,
)
from simple_login.models import KEY_DEFAULT_VALUE


class CustomAPIView(APIView):
    user_model = None


class RequestActivationKey(CustomAPIView):
    serializer_class = ActivationKeyRequestSerializer

    def send_activation_code(self, email):
        key = generate_random_key()
        user = self.user_model.objects.get(email=email)
        user.account_activation_key = key
        user.save()
        send_account_activation_email(email, key)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.send_activation_code(serializer.data.get('email'))
        return Response(status=status.HTTP_200_OK)


class ActivateAccount(CustomAPIView):
    serializer_class = AccountActivationSerializer

    def activate(self, email):
        user = self.user_model.objects.get(email=email)
        user.is_active = True
        user.account_activation_key = KEY_DEFAULT_VALUE
        user.save()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.activate(serializer.data.get('email'))
        return Response(status=status.HTTP_200_OK)


class Login(CustomAPIView):
    serializer_class = LoginSerializer

    def get_token(self, email):
        user = self.user_model.objects.get(email=email)
        token = Token.objects.get(user=user)
        return token.key

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        login_key = self.get_token(serializer.data.get('email'))
        return Response(
            data={'token': login_key},
            status=status.HTTP_200_OK
        )


class RequestPasswordReset(CustomAPIView):
    serializer_class = PasswordResetRequestSerializer

    def send_password_reset_key(self, email):
        user = self.user_model.objects.get(email=email)
        key = generate_random_key()
        user.password_reset_key = key
        user.save()
        send_password_reset_email(email, key)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.send_password_reset_key(serializer.data.get('email'))
        return Response(status=status.HTTP_200_OK)


class ChangePassword(CustomAPIView):
    serializer_class = PasswordChangeSerializer

    def change(self, email, new_password):
        user = self.user_model.objects.get(email=email)
        user.set_password(new_password)
        user.password_reset_key = KEY_DEFAULT_VALUE
        user.save()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            user_model=self.user_model,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.change(
            serializer.data.get('email'),
            serializer.data.get('new_password')
        )
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
