import threading

from django.conf import settings
from django.core.mail import send_mail


def _send_mail_in_worker_thread(
        title,
        body,
        recipients,
        auth_user=settings.EMAIL_HOST_USER,
        fail_silently=False
):
    threading.Thread(
        target=send_mail,
        args=(title, body, auth_user, recipients),
        kwargs={'fail_silently': fail_silently}
    ).start()


def send_password_reset_email(email, key):
    _send_mail_in_worker_thread(
        '{}: Password reset'.format(settings.APP_NAME),
        'Password reset key: {}'.format(key),
        [str(email)]
    )


def send_activation_email(email, key):
    _send_mail_in_worker_thread(
        '{}: Account activation'.format(settings.APP_NAME),
        'Account activation key: {}'.format(key),
        [str(email)]
    )
