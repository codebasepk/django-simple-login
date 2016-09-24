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

import threading

from django.conf import settings
from django.core.mail import send_mail


def _send_mail_in_worker_thread(
        title,
        body,
        recipients,
        auth_user=settings.EMAIL_HOST_USER,
        fail_silently=False
):
    threading.Thread(
        target=send_mail,
        args=(title, body, auth_user, recipients),
        kwargs={'fail_silently': fail_silently}
    ).start()


def send_password_reset_email(email, key):
    _send_mail_in_worker_thread(
        '{}: Password reset'.format(settings.APP_NAME),
        'Password reset key: {}'.format(key),
        [str(email)]
    )


def send_activation_email(email, key):
    _send_mail_in_worker_thread(
        '{}: Account activation'.format(settings.APP_NAME),
        'Account activation key: {}'.format(key),
        [str(email)]
    )
