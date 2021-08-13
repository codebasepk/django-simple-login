# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
# Simple Login
# Copyright (C) CODEBASE
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

from rest_framework.authentication import TokenAuthentication
from simple_login.models.api import Tokens
from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import exceptions
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(days=settings.TOKEN_EXPIRED_AFTER_DAYS) - time_elapsed
    return left_time


def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
    return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    model = Tokens

    def authenticate_credentials(self, key):

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")

        return token.user, token
