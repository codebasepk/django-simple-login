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

from rest_framework import permissions
from rest_framework.views import APIView

from simple_login.utils import UserHelpers


class BaseAPIView(APIView):
    user_model = None
    serializer = None
    serializer_class = None
    validation_class = None

    def post(self, *args, **kwargs):
        """Validate parameters for a request.

        Ensure to call super().post(*args, **kwargs) when this method is
        overridden.
        """
        self.validate_request_parameters()

    def put(self, *args, **kwargs):
        """Validate parameters for a request.

        Ensure to call super().put(*args, **kwargs) when this method is
        overridden.
        """
        self.validate_request_parameters()

    @property
    def user_account(self):
        """Return account helpers object by reading email from serializer
        data."""
        return UserHelpers(self.user_model, self.serializer.data.get('email'))

    def get_user(self):
        if not self.request.user.is_anonymous():
            return self.get_auth_user()
        return self.user_account.user

    def get_auth_user(self):
        return self.request.user

    def get_serializer_class(self):
        """Return the data serializer class.

        One may override this method to return custom serializer class.
        """
        return self.serializer_class

    def get_validation_class(self):
        return self.validation_class

    def get_user_model(self):
        """Return the User account model.

        One may override this method to return a custom user account model.
        """
        return self.user_model

    def validate_request_parameters(self, raise_exception=True):
        if self.validation_class:
            serializer_class = self.get_validation_class()
        else:
            serializer_class = self.get_serializer_class()
        self.serializer = serializer_class(
            user_model=self.user_model,
            data=self.request.data
        )
        self.serializer.is_valid(raise_exception=raise_exception)


class ProfileBaseAPIView(BaseAPIView):
    def get_user_profile_data_with_token(self):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=self.user_account.user)
        data = serializer.data
        data.update({'token': self.user_account.get_auth_token()})
        return data


class AuthenticatedRequestBaseAPIView(BaseAPIView):
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
