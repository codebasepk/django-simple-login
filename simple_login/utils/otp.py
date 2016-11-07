from django.conf import settings


class OTPHandler:
    def __init__(self, user_model_instance):
        from simple_login.models import BaseUser
        if not isinstance(user_model_instance, BaseUser):
            raise ValueError(
                'Parameter `user_model_instance` must be an instance of '
                'simple_login.models.BaseUser'
            )
        self.instance = user_model_instance

    def _hasattr(self, attr):
        return getattr(self.instance, attr) is not None

    def _split_country_code_and_number(self):
        num = getattr(self.instance, settings.ACCOUNT_MOBILE_NUMBER_FIELD)
        country_code, mobile_number = tuple(num.split('-'))
        if country_code.startswith('+'):
            country_code = country_code.replace('+', '')
        return country_code, mobile_number

    def generate_and_send_account_activation_otps(self, commit=False):
        if self._hasattr('account_activation_sms_otp'):
            self.instance.account_activation_sms_otp = \
                self.generate_sms_otp(*self._split_country_code_and_number())
        if self._hasattr('account_activation_email_otp'):
            from simple_login.utils import send_activation_email
            self.instance.account_activation_email_otp = \
                self.generate_email_otp()
            send_activation_email(
                self.instance.email,
                self.instance.account_activation_email_otp
            )
        if commit:
            self.instance.save()

    @staticmethod
    def _get_email_otp_generator():
        try:
            return settings.ACCOUNT_ACTIVATION_EMAIL_OTP_CALLABLE
        except AttributeError:
            from simple_login.utils import generate_random_key
            return generate_random_key

    @staticmethod
    def generate_email_otp():
        return OTPHandler._get_email_otp_generator()()

    @staticmethod
    def _get_sms_otp_generator():
        try:
            return settings.ACCOUNT_ACTIVATION_SMS_OTP_CALLABLE
        except AttributeError:
            return None

    @staticmethod
    def generate_sms_otp(country_code, mobile_number):
        return OTPHandler._get_sms_otp_generator()(country_code, mobile_number)
