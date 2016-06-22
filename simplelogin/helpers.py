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

import random
import threading

from django.conf import settings
from django.core.mail import send_mail


def generate_random_key():
    # Ensures the returned number is always 5 numbers long.
    return random.randint(10000, 99999)


def _send_account_activation_email(email, key):
    send_mail(
        '{}: Account activation'.format(settings.APP_NAME),
        'Account activation key: {}'.format(key),
        settings.EMAIL_HOST_USER,
        [str(email)],
        fail_silently=False
    )


def send_account_activation_email(email, key):
    thread = threading.Thread(
        target=_send_account_activation_email, args=(email, key))
    thread.start()


def _send_password_reset_email(email, key):
    send_mail(
        '{}: Password reset'.format(settings.APP_NAME),
        'Password reset key: {}'.format(key),
        settings.EMAIL_HOST_USER,
        [str(email)],
        fail_silently=False
    )


def send_password_reset_email(email, key):
    thread = threading.Thread(
        target=_send_password_reset_email, args=(email, key))
    thread.start()
