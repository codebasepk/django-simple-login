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

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status, permissions

from sample_app.serializers import UserProfileSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserProfileSerializer


class UserDetailsView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(instance=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
