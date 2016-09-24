from rest_framework.authtoken.models import Token

from simple_login.utils import (
    generate_random_key,
    send_password_reset_email,
    send_activation_email,
)

KEY_DEFAULT_VALUE = -1


class UserHelpers:
    def __init__(self, user_model, email):
        self.user = user_model.objects.get(email=email)

    def _generate_and_save_password_reset_key(self):
        key = generate_random_key()
        self._set_password_reset_key(key)
        return key

    def _set_password_reset_key(self, key):
        self.user.password_reset_key = key
        self.user.save()

    def _get_email(self):
        return self.user.email

    def generate_and_send_password_reset_key(self):
        key = self._generate_and_save_password_reset_key()
        send_password_reset_email(self._get_email(), key)

    def change_password(self, new_password):
        self.user.set_password(new_password)
        self.user.password_reset_key = KEY_DEFAULT_VALUE
        self.user.save()

    def get_auth_token(self):
        return Token.objects.get(user=self.user).key

    def activate(self):
        self.user.is_active = True
        self.user.account_activation_key = KEY_DEFAULT_VALUE
        self.user.save()

    def _generate_and_save_account_activation_key(self):
        key = generate_random_key()
        self.user.account_activation_key = key
        self.user.save()
        return key

    def generate_and_send_account_activation_key(self):
        key = self._generate_and_save_account_activation_key()
        send_activation_email(self.user.email, key)
