#
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

from django.db import models

from simple_login import models as dsl_models


class User(dsl_models.BaseUser):
    full_name = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=255, blank=False)
    account_activation_sms_otp = None
    password_reset_sms_otp = None
