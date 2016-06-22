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

from django.contrib.auth.models import BaseUserManager


def _raise_if_email_or_password_missing(email, password):
    if not email and not password:
        raise ValueError('Email and Password are mandatory.')

    if not email:
        raise ValueError('Email is mandatory.')

    if not password:
        raise ValueError('Password is mandatory.')


class SimpleUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        _raise_if_email_or_password_missing(email, password)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, is_admin=True, **extra_fields)
