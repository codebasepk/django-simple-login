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

import inspect

from rest_framework.authtoken.models import Token

from simple_login import KEY_DEFAULT_VALUE
from simple_login.utils import (
    generate_random_key,
    send_password_reset_email,
    send_activation_email,
)


class UserHelpers:
    def __init__(self, model_class_or_instance, email=None):
        if inspect.isclass(model_class_or_instance):
            if not email:
                raise ValueError('Argument `email` is required')
            self.user = model_class_or_instance.objects.get(email=email)
        else:
            self.user = model_class_or_instance

    def commit_changes(self):
        self.user.save()

    def _generate_and_save_password_reset_email_otp(self):
        key = generate_random_key()
        self._set_password_reset_email_otp(key)
        return key

    def _set_password_reset_email_otp(self, key):
        self.user.password_reset_email_otp = key
        self.user.save()

    def _get_email(self):
        return self.user.email

    def generate_and_send_password_reset_email_otp(self):
        key = self._generate_and_save_password_reset_email_otp()
        send_password_reset_email(self._get_email(), key)

    def hash_password(self, commit=True):
        self.user.set_password(self.user.password)
        if commit:
            self.commit_changes()

    def change_password(self, new_password, commit=True):
        self.user.set_password(new_password)
        self.user.password_reset_email_otp = KEY_DEFAULT_VALUE
        if commit:
            self.user.save()

    def generate_auth_token(self):
        Token.objects.create(user=self.user)

    def get_auth_token(self):
        return Token.objects.get(user=self.user).key

    def activate(self, commit=True):
        self.user.is_active = True
        self.user.account_activation_email_otp = KEY_DEFAULT_VALUE
        self.user.account_activation_sms_otp = KEY_DEFAULT_VALUE
        if commit:
            self.user.save()

    def _generate_and_save_account_activation_email_otp(self):
        key = generate_random_key()
        self.user.account_activation_email_otp = key
        self.user.save()
        return key

    def generate_and_send_account_activation_email_otp(self):
        send_activation_email(
            self.user.email,
            self._generate_and_save_account_activation_email_otp()
        )

    def is_active(self):
        return self.user.is_active

    def set_active(self, boolean, commit=True):
        self.user.is_active = boolean
        if commit:
            self.commit_changes()

    def is_admin(self):
        return self.user.is_admin
