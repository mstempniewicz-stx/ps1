import logging
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class MyUserManager(BaseUserManager):
    def _create_user(
        self,
        email,
        password,
        first_name,
        last_name,
        is_staff,
        is_superuser,
        **extra_fields,
    ):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(
            email,
            password,
            first_name,
            last_name,
            is_staff=False,
            is_superuser=False,
            **extra_fields,
        )

    def create_superuser(
        self, email, first_name="", last_name="", password=None, **extra_fields
    ):
        return self._create_user(
            email,
            password,
            first_name,
            last_name,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    app_label = "accounts"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    email = models.EmailField(_("Email address"), unique=True)

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)

    activation_key = models.UUIDField(unique=True, default=uuid.uuid4)  # email
    confirmed_email = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = MyUserManager()

    def __str__(self):
        return f"{self.id} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def confirm_email(self):
        expiration_date = self.date_joined + timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS
        )
        activation_expired = expiration_date < timezone.now()
        if not activation_expired and not self.confirmed_email:
            self.confirmed_email = True
            self.save()
            return True
        return False
