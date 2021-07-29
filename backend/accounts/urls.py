from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import (
    ChangePasswordView,
    RequestPasswordResetView,
    ResetPasswordView,
    UserConfirmEmailView,
    UserEmailConfirmationStatusView,
    UserOwnAccountView,
    UserRegisterView,
)

urlpatterns = [
    url(_(r"^register/$"), UserRegisterView.as_view(), name="register"),
    url(_(r"^me/$"), UserOwnAccountView.as_view(), name="me"),
    url(
        _(r"^confirm/email/(?P<activation_key>.*)/$"),
        UserConfirmEmailView.as_view(),
        name="confirm_email",
    ),
    url(
        _(r"^status/email/$"), UserEmailConfirmationStatusView.as_view(), name="status"
    ),
    url(_(r"^change/password/$"), ChangePasswordView.as_view(), name="password_change"),
    url(
        _(r"^password/reset/request/$"),
        RequestPasswordResetView.as_view(),
        name="request_password_reset",
    ),
    url(_(r"^password/reset/$"), ResetPasswordView.as_view(), name="password_reset"),
]
