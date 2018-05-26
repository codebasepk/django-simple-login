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

import json
import tempfile
from urllib.request import urlretrieve

from django.conf import settings
from django.urls import get_callable
from django.contrib.auth import get_user_model
from django.core.files import File
from rest_framework import generics, exceptions, status, response, views
from rest_framework.authtoken.models import Token

from simple_login.serializers import (
    ActivationKeyRequestSerializer,
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
    StatusSerializer,
    ActivationValidationSerializer,
    LoginSerializer,
    RetrieveUpdateDestroyProfileValidationSerializer,
)
from simple_login.views.base import (
    BaseAPIView,
    ProfileBaseAPIView,
    AuthenticatedRequestBaseAPIView,
)
from simple_login import models
from simple_login.utils.otp import OTPHandler
from simple_login.utils.auth import AuthMethod
from simple_login.utils import social
from simple_login.utils.user import UserHelpers
from simple_login import serializers


SERIALIZER = get_callable(settings.AUTH_USER_SERIALIZER) if settings.AUTH_USER_SERIALIZER else \
    serializers.AuthUserSerializer


def get_unique_username(user_model, username_desired, append_id=0):
    username = username_desired
    if user_model.objects.filter(username=username).count() > 0:
        username = '{}-{}'.format(username, append_id)
        get_unique_username(user_model, username, append_id)
    return username


def download_and_set_photo(url, instance, field, is_facebook=False):
    if is_facebook:
        filename = url.split('?')[0].split('/')[-1]
    else:
        filename = url.split('/')[-1]
    with tempfile.NamedTemporaryFile(suffix=filename.split('.')[-1]) as f:
        urlretrieve(url, filename=f.name)
        getattr(instance, field).save(filename, File(f))


class TwitterLoginAPIView(views.APIView):
    def post(self, *args, **kwargs):
        validator = serializers.TwitterLoginSerializer(data=self.request.data)
        validator.is_valid(True)
        resp, data = social.login_twitter(validator.data.get('access_token'),
                                          validator.data.get('access_token_secret'))
        if resp['status'] == str(status.HTTP_200_OK):
            data_json = json.loads(data.decode())
            obj, created = models.TwitterLink.objects.get_or_create(unique_id=data_json['id_str'])
            if created:
                user = get_user_model().objects.create_user(
                    username=get_unique_username(get_user_model(),
                                                 data_json['screen_name'].lower()))
                name = data_json.get('name', '')
                if name:
                    if hasattr(user, 'full_name'):
                        user.full_name = name
                    elif hasattr(user, 'first_name') and hasattr(user, 'last_name'):
                        splitted = name.split(' ')
                        user.first_name = splitted[0]
                        if len(splitted) > 1:
                            user.last_name = splitted[1]
                if hasattr(user, 'photo') and data_json.get('profile_image_url', ''):
                    url = data_json['profile_image_url'].replace('_normal', '')
                    download_and_set_photo(url, user, 'photo')
                obj.user = user
                obj.save()
                serializer = SERIALIZER(instance=user)
                d = serializer.data
                d.update({'token': Token.objects.get(user=obj.user).key})
                return response.Response(data=d, status=status.HTTP_201_CREATED)
            serializer = SERIALIZER(instance=obj.user)
            d = serializer.data
            d.update({'token': Token.objects.get(user=obj.user).key})
            return response.Response(data=d, status=status.HTTP_200_OK)
        return response.Response(data=json.loads(data.decode()),
                                 status=status.HTTP_400_BAD_REQUEST)


class FacebookLoginAPIView(views.APIView):
    def post(self, *args, **kwargs):
        validator = serializers.FacebookLoginSerializer(data=self.request.data)
        validator.is_valid(True)
        resp = social.login_facebook(validator.data.get('access_token'))
        if resp.status_code == status.HTTP_200_OK:
            data_json = resp.json()
            obj, created = models.FacebookLink.objects.get_or_create(unique_id=data_json['id'])
            if created:
                user = get_user_model().objects.create_user(
                    username=get_unique_username(get_user_model(),
                                                 data_json['first_name'].lower()))
                first_name = data_json['first_name']
                last_name = data_json['last_name']
                if hasattr(user, 'full_name'):
                    user.full_name = '{} {}'.format(first_name, last_name)
                elif hasattr(user, 'first_name') and hasattr(user, 'last_name'):
                    user.first_name = first_name
                    user.last_name = last_name
                if hasattr(user, 'photo') and data_json['picture']['data']['url']:
                    download_and_set_photo(data_json['picture']['data']['url'], user, 'photo', True)
                obj.user = user
                obj.save()
                serializer = SERIALIZER(instance=user)
                d = serializer.data
                d.update({'token': Token.objects.get(user=obj.user).key})
                return response.Response(data=d, status=status.HTTP_201_CREATED)
            serializer = SERIALIZER(instance=obj.user)
            d = serializer.data
            d.update({'token': Token.objects.get(user=obj.user).key})
            return response.Response(data=d, status=status.HTTP_200_OK)
        return response.Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        if AuthMethod.email_only() and 'email' not in self.request.data:
            raise exceptions.ValidationError({'email': ['This field is required.']})
        elif AuthMethod.username_only() and 'username' not in self.request.data:
            raise exceptions.ValidationError({'username': ['This field is required.']})
        elif 'email' not in self.request.data and 'username' not in self.request.data:
            raise exceptions.ValidationError('Must provide either `email` or `username`')
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED and not AuthMethod.email_only():
            response.data.update(
                {'token': UserHelpers(get_user_model(),
                                      id=int(response.data['id'])).get_auth_token()})
        return response


class ActivationAPIView(ProfileBaseAPIView):
    validation_class = ActivationValidationSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.activate()
        return response.Response(data=self.get_user_profile_data_with_token(),
                                 status=status.HTTP_200_OK)


class ActivationKeyRequestAPIView(BaseAPIView):
    validation_class = ActivationKeyRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        otp_handler = OTPHandler(self.get_user())
        otp_handler.generate_and_send_account_activation_otps(commit=True)
        return response.Response(status=status.HTTP_200_OK)


class LoginAPIView(ProfileBaseAPIView):
    validation_class = LoginSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return response.Response(data=self.get_user_profile_data_with_token(), status=status.HTTP_200_OK)


class PasswordResetRequestAPIView(BaseAPIView):
    validation_class = PasswordResetRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.generate_and_send_password_reset_email_otp()
        return response.Response(status=status.HTTP_200_OK)


class PasswordChangeAPIView(BaseAPIView):
    validation_class = PasswordChangeSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.change_password(self.serializer.data.get('new_password'))
        return response.Response(status=status.HTTP_200_OK)


class StatusAPIView(BaseAPIView):
    validation_class = StatusSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return response.Response(status=status.HTTP_200_OK)


class RetrieveUpdateDestroyProfileAPIView(AuthenticatedRequestBaseAPIView):
    validation_class = RetrieveUpdateDestroyProfileValidationSerializer
    http_method_names = ['put', 'patch', 'get', 'delete']

    def get(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.get_auth_user())
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        self.get_auth_user().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, *args, **kwargs):
        super().put(*args, **kwargs)
        serializer = self.update_fields_with_request_data()
        self.ensure_password_hashed()
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
