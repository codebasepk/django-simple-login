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

from rest_framework import generics

from simple_login import views
from sample_app import models
from sample_app import serializers


class Register(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class Activate(views.ActivationAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ActivationKeyRequest(views.ActivationKeyRequestAPIView):
    user_model = models.User


class Login(views.LoginAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class Profile(views.RetrieveUpdateDestroyProfileAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ForgotPassword(views.PasswordResetRequestAPIView):
    user_model = models.User


class ChangePassword(views.PasswordChangeAPIView):
    user_model = models.User


class Status(views.StatusAPIView):
    user_model = models.User
