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

from simple_login import views
from sample_app import models
from sample_app import serializers


class RegisterAPIView(views.RegisterAPIView):
    serializer_class = serializers.UserSerializer


class ActivateAPIView(views.ActivationAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ActivationKeyRequestAPIView(views.ActivationKeyRequestAPIView):
    user_model = models.User


class LoginAPIView(views.LoginAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ProfileAPIView(views.RetrieveUpdateDestroyProfileAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ForgotPasswordAPIView(views.PasswordResetRequestAPIView):
    user_model = models.User


class ChangePasswordAPIView(views.PasswordChangeAPIView):
    user_model = models.User


class StatusAPIView(views.StatusAPIView):
    user_model = models.User
