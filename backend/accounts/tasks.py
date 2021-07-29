import logging

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from .models import User

logger = logging.getLogger(__name__)


@shared_task
def send_reset_password_email_task(email):
    user = None
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        logger.warning(
            f"User with mail {email} not in database. Not sending reset password email."
        )

    if user:
        link = settings.FRONTEND_RESET_PASSWORD_URL.format(
            activation_key=user.activation_key
        )
        subject = _("Reset password")
        message = _(f"Click here to reset your password: {link}")
        html_message = loader.render_to_string(
            "reset_password_email.html",
            {"link": link},
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
