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

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from simple_login.serializers import (
    ActivationKeyRequestSerializer,
    AccountActivationValidationSerializer,
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


class AccountActivationAPIView(CustomAPIView):
    serializer_class = None

    def get_serializer_class(self):
        raise NotImplemented('Please implement this method on inheritance.')

    def _get_serializer_class(self):
        return self.serializer_class or self.get_serializer_class()

    def post(self, request, *args, **kwargs):
        # Make sure the request parameters are valid and activate
        # the user account.
        self.serializer = AccountActivationValidationSerializer(
            user_model=self.user_model,
            data=request.data
        )
        self.serializer.is_valid(raise_exception=True)
        self.user_account.activate()
        # We want to return user details, including the login
        # token on activation of the account, so lets formulate
        # that.
        serializer_class = self._get_serializer_class()
        serializer = serializer_class(instance=self.user_account.user)
        data = serializer.data
        data.update({'token': self.user_account.get_auth_token()})
        return Response(data=data, status=status.HTTP_200_OK)


class LoginAPIView(CustomAPIView):
    serializer_class = None

    def get_serializer_class(self):
        raise NotImplemented('Please implement this method on inheritance.')

    def _get_serializer_class(self):
        return self.serializer_class or self.get_serializer_class()

    def post(self, request, *args, **kwargs):
        self.serializer = LoginSerializer(
            user_model=self.user_model,
            data=request.data
        )
        self.serializer.is_valid(raise_exception=True)
        serializer_class = self._get_serializer_class()
        serializer = serializer_class(instance=self.user_account.user)
        data = serializer.data
        data.update({'token': self.user_account.get_auth_token()})
        return Response(data=data, status=status.HTTP_200_OK)


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


class RetrieveUpdateDestroyProfileView(APIView):
    serializer_class = None
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['put', 'get', 'delete']

    def get_auth_user(self):
        return self.request.user

    def get_serializer_class(self):
        raise NotImplemented('Please implement this method on inheritance.')

    def _get_serializer_class(self):
        return self.serializer_class or self.get_serializer_class()

    def get(self, *args, **kwargs):
        serializer_class = self._get_serializer_class()
        serializer = serializer_class(self.get_auth_user())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        user = self.get_auth_user()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, *args, **kwargs):
        email = self.request.data.get('email')
        if email:
            return Response(
                {'email': 'Not allowed to change email.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer_class = self._get_serializer_class()
        serializer = serializer_class(
            instance=self.request.user,
            data=self.request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Make sure to hash the password, in case it was changed.
        password = self.request.data.get('password')
        if password:
            self.request.user.set_password(password)
            self.request.user.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
