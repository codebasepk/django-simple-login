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

from simple_login.utils import send_activation_email, generate_random_key


class OTPHandler:
    def __init__(self, user_model_instance):
        self.instance = user_model_instance

    def _hasattr(self, attr):
        return self._getattr(attr) is not None

    def _getattr(self, attr):
        return getattr(self.instance, attr)

    def _setattr(self, key, value):
        setattr(self.instance, key, value)

    def generate_and_send_account_activation_otps(self, commit=False):
        if self._hasattr('account_activation_sms_otp'):
            self._setattr(
                'account_activation_sms_otp',
                self.generate_sms_otp(
                    self._getattr(settings.ACCOUNT_MOBILE_NUMBER_FIELD))
            )
        if self._hasattr('account_activation_email_otp'):
            self._setattr(
                'account_activation_email_otp',
                self.generate_email_otp()
            )
            send_activation_email(
                self.instance.email,
                self.instance.account_activation_email_otp
            )
        if commit:
            self.instance.save()

    @staticmethod
    def _get_email_otp_generator():
        try:
            return settings.ACCOUNT_ACTIVATION_EMAIL_OTP_CALLABLE
        except AttributeError:
            return generate_random_key

    @staticmethod
    def generate_email_otp():
        return OTPHandler._get_email_otp_generator()()

    @staticmethod
    def _get_sms_otp_generator():
        try:
            return settings.ACCOUNT_ACTIVATION_SMS_OTP_CALLABLE
        except AttributeError:
            return None

    @staticmethod
    def generate_sms_otp(mobile_number):
        return OTPHandler._get_sms_otp_generator()(mobile_number)
