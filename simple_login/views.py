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
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
    StatusSerializer,
    AccountActivationValidationSerializer,
    LoginSerializer,
    RetrieveUpdateDestroyValidationSerializer,
)
from simple_login.helpers import AccountHelpers


class BaseAPIView(APIView):
    user_model = None
    child_model = None
    serializer = None
    child_serializer = None
    serializer_class = None
    child_serializer_class = None
    validation_class = None

    def post(self, *args, **kwargs):
        """Validate parameters for a request.

        Ensure to call super().post(*args, **kwargs) when this
        method is over-ridden.
        """
        self.validate_request_parameters()

    def put(self, *args, **kwargs):
        """Validate parameters for a request.

        Ensure to call super().put(*args, **kwargs) when this
        method is over-ridden.
        """
        self.validate_request_parameters()

    @property
    def user_account(self):
        """
        Return account helpers object by reading email from
        serializer data.
        """
        email = self.serializer.data.get('email')
        return AccountHelpers(self.user_model, email)

    def get_user(self):
        if not self.request.user.is_anonymous():
            return self.get_auth_user()
        return self.user_account.user

    def get_auth_user(self):
        return self.request.user

    def get_serializer_class(self):
        """Return the data serializer class.

        One may over-ride this method to return custom
        serializer class.
        """
        return self.serializer_class

    def get_child_serializer_class(self):
        return self.child_serializer_class

    def get_child_parent_relation_key(self):
        return 'user'

    def get_user_model(self):
        """Return the User account model.

        One may over-ride this method to return a custom
        user account model.
        """
        return self.user_model

    def get_child_model(self):
        return self.child_model

    def validate_request_parameters(self, raise_exception=True):
        if self.validation_class:
            serializer_class = self.validation_class
        else:
            serializer_class = self.get_serializer_class()
        self.serializer = serializer_class(
            user_model=self.user_model,
            data=self.request.data
        )
        self.serializer.is_valid(raise_exception=raise_exception)


class RequestActivationKey(BaseAPIView):
    validation_class = ActivationKeyRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.generate_and_send_account_activation_key()
        return Response(status=status.HTTP_200_OK)


class UserProfileBase(BaseAPIView):
    def get_user_profile(self, token=True):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=self.get_user())
        data = serializer.data
        if token:
            data.update({'token': self.user_account.get_auth_token()})
        child_serializer_class = self.get_child_serializer_class()
        if child_serializer_class:
            child_model = self.get_child_model()
            instance = child_model.objects.get(user=self.get_user())
            child_serializer = child_serializer_class(instance)
            data.update(child_serializer.data)
        return data


class AccountActivationAPIView(UserProfileBase):
    validation_class = AccountActivationValidationSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.activate()
        data = self.get_user_profile()
        return Response(data=data, status=status.HTTP_200_OK)


class LoginAPIView(UserProfileBase):
    validation_class = LoginSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        data = self.get_user_profile()
        return Response(data=data, status=status.HTTP_200_OK)


class RequestPasswordReset(BaseAPIView):
    validation_class = PasswordResetRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.generate_and_send_password_reset_key()
        return Response(status=status.HTTP_200_OK)


class ChangePassword(BaseAPIView):
    validation_class = PasswordChangeSerializer

    def change(self):
        new_password = self.serializer.data.get('new_password')
        self.user_account.change_password(new_password)

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.change()
        return Response(status=status.HTTP_200_OK)


class AccountStatus(BaseAPIView):
    validation_class = StatusSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return Response(status=status.HTTP_200_OK)


class _AuthenticatedRequestBase(UserProfileBase):
    permission_classes = (permissions.IsAuthenticated, )

    def ensure_password_hashed(self):
        password = self.request.data.get('password')
        if password:
            self.request.user.set_password(password)
            self.request.user.save()

    def update_fields_with_request_data(self):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            instance=self.request.user,
            data=self.request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer


class RetrieveUpdateDestroyProfileView(_AuthenticatedRequestBase):
    validation_class = RetrieveUpdateDestroyValidationSerializer
    http_method_names = ['put', 'get', 'delete']

    def get(self, *args, **kwargs):
        data = self.get_user_profile(token=False)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        user = self.get_user()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, *args, **kwargs):
        super().put(*args, **kwargs)
        serializer = self.update_fields_with_request_data()
        self.ensure_password_hashed()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
