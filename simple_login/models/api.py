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

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.db.models.signals import post_save

from simple_login import KEY_DEFAULT_VALUE
from simple_login.managers import SimpleUserManager
from simple_login.models.utils import process_save


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, blank=False, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, blank=False)

    # OTP records.
    account_activation_email_otp = models.IntegerField(
        default=KEY_DEFAULT_VALUE
    )
    account_activation_sms_otp = models.IntegerField(
        default=KEY_DEFAULT_VALUE
    )
    password_reset_email_otp = models.IntegerField(
        default=KEY_DEFAULT_VALUE
    )
    password_reset_sms_otp = models.IntegerField(
        default=KEY_DEFAULT_VALUE
    )

    objects = SimpleUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        abstract = True


post_save.connect(process_save, sender=settings.AUTH_USER_MODEL)
