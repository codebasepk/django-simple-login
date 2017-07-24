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

from sample_app import views


urlpatterns = [
    url(r'^api/register$', views.Register.as_view()),
    url(r'^api/request-activation-key$', views.ActivationKeyRequest.as_view()),
    url(r'^api/activate$', views.Activate.as_view()),
    url(r'^api/login$', views.Login.as_view()),
    url(r'^api/forgot-password$', views.ForgotPassword.as_view()),
    url(r'^api/change-password$', views.ChangePassword.as_view()),
    url(r'^api/status$', views.Status.as_view()),
    url(r'^api/me$', views.Profile.as_view()),
]
