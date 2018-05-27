from django.conf import settings
from rest_framework.exceptions import ValidationError

from simple_login import AUTH_METHOD_EMAIL, AUTH_METHOD_USERNAME, AUTH_METHOD_EMAIL_USERNAME


class AuthMethod:
    @staticmethod
    def email_only():
        if not hasattr(settings, 'ACCOUNT_AUTH_METHOD'):
            return True
        return settings.ACCOUNT_AUTH_METHOD == AUTH_METHOD_EMAIL

    @staticmethod
    def username_only():
        if not hasattr(settings, 'ACCOUNT_AUTH_METHOD'):
            return False
        return settings.ACCOUNT_AUTH_METHOD == AUTH_METHOD_USERNAME

    @staticmethod
    def email_or_username():
        if not hasattr(settings, 'ACCOUNT_AUTH_METHOD'):
            return False
        return settings.ACCOUNT_AUTH_METHOD == AUTH_METHOD_EMAIL_USERNAME


def get_query(data):
    assert isinstance(data, dict)
    if AuthMethod.email_only():
        if 'email' not in data:
            raise ValidationError('`email` is required')
        query = {'email': data['email']}
    elif AuthMethod.username_only():
        if 'username' not in data:
            raise ValidationError('`username` is required')
        query = {'username': data['username']}
    elif AuthMethod.email_or_username():
        if 'username' in data and 'email' not in data:
            query = {'username': data['username']}
        elif 'username' not in data and 'email' in data:
            query = {'email': data['email']}
        elif 'username' in data and 'email' in data:
            query = {'username': data['username'], 'email': data['email']}
        else:
            raise ValidationError('`username` or `email` must be provided')
    else:
        query = {}
    return query
