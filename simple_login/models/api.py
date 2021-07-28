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

import os
import binascii

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from simple_login import KEY_DEFAULT_VALUE
from simple_login.models.utils import process_save
from simple_login.managers import SimpleUserManager


class Tokens(Token):
    """
    The default authorization token model.
    """
    key = models.CharField("Key", max_length=40, db_index=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name="User"
    )
    created = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class TwitterLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    unique_id = models.CharField(max_length=255, blank=False)


class FacebookLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    unique_id = models.CharField(max_length=255, blank=False)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, blank=True, unique=True, null=True)
    email = models.EmailField(max_length=255, blank=True, unique=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=False)

    # OTP records.
    account_activation_email_otp = models.IntegerField(default=KEY_DEFAULT_VALUE)
    account_activation_sms_otp = models.IntegerField(default=KEY_DEFAULT_VALUE)
    password_reset_email_otp = models.IntegerField(default=KEY_DEFAULT_VALUE)
    password_reset_sms_otp = models.IntegerField(default=KEY_DEFAULT_VALUE)

    objects = SimpleUserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.username if self.username else self.email

    def get_short_name(self):
        return self.username if self.username else self.email

    def __str__(self):
        return self.username if self.username else self.email

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
