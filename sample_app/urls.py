# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

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

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from sample_app import views


urlpatterns = [
    url(r'^api/register$', views.RegisterAPIView.as_view()),
    url(r'^api/request-activation-key$', views.ActivationKeyRequestAPIView.as_view()),
    url(r'^api/activate$', views.ActivateAPIView.as_view()),
    url(r'^api/login$', views.LoginAPIView.as_view()),
    url(r'^api/logout$', views.Logout.as_view()),
    url(r'^api/forgot-password$', views.ForgotPasswordAPIView.as_view()),
    url(r'^api/change-password$', views.ChangePasswordAPIView.as_view()),
    url(r'^api/status$', views.StatusAPIView.as_view()),
    url(r'^api/me$', views.ProfileAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
