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

from rest_framework.generics import CreateAPIView

from simple_login.views import (
    ActivationKeyRequestAPIView,
    RetrieveUpdateDestroyProfileAPIView,
    ActivationAPIView,
    LoginAPIView,
    PasswordResetRequestAPIView,
    PasswordChangeAPIView,
    StatusAPIView,
)

from sample_app.models import User
from sample_app.serializers import UserSerializer


class Register(CreateAPIView):
    serializer_class = UserSerializer


class Activate(ActivationAPIView):
    user_model = User
    serializer_class = UserSerializer


class ActivationKeyRequest(ActivationKeyRequestAPIView):
    user_model = User
    serializer_class = UserSerializer


class Login(LoginAPIView):
    user_model = User
    serializer_class = UserSerializer


class Profile(RetrieveUpdateDestroyProfileAPIView):
    user_model = User
    serializer_class = UserSerializer


class ForgotPassword(PasswordResetRequestAPIView):
    user_model = User
    serializer_class = UserSerializer


class ChangePassword(PasswordChangeAPIView):
    user_model = User
    serializer_class = UserSerializer


class Status(StatusAPIView):
    user_model = User
    serializer_class = UserSerializer
