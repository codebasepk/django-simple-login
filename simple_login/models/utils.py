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

from simple_login.utils import UserHelpers, OTPHandler


def process_save(sender, instance=None, created=False, **kwargs):
    if created:
        user = UserHelpers(instance)
        user.generate_auth_token()
        if user.is_admin():
            if not user.is_active():
                user.set_active(True, commit=False)
        else:
            user.hash_password(commit=False)
            if not user.is_active():
                otp_handler = OTPHandler(instance)
                otp_handler.generate_and_send_account_activation_otps()
        user.commit_changes()
