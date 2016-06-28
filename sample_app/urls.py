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

from django.conf.urls import url
from simple_login.views import (
    RequestActivationKey,
    RequestPasswordReset,
    ChangePassword,
    AccountStatus,
)
from sample_app import views as experimental_views
from sample_app.models import UserProfile


urlpatterns = [
    url(
        r'^api/sample/register$',
        experimental_views.RegisterUser.as_view()
    ),
    url(
        r'^api/sample/request$',
        RequestActivationKey.as_view(user_model=UserProfile)
    ),
    url(
        r'^api/sample/activate$',
        experimental_views.ActivateAccount.as_view(user_model=UserProfile)
    ),
    url(
        r'^api/sample/login$',
        experimental_views.Login.as_view(user_model=UserProfile)
    ),
    url(
        r'^api/sample/reset$',
        RequestPasswordReset.as_view(user_model=UserProfile)
    ),
    url(
        r'^api/sample/change$',
        ChangePassword.as_view(user_model=UserProfile)
    ),
    url(
        r'^api/sample/status$',
        AccountStatus.as_view(user_model=UserProfile)
    ),
    url(
        r'^api/sample/me',
        experimental_views.UserProfile.as_view(user_model=UserProfile)
    ),
]
