import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import AtomicMixin

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)
from .tasks import send_reset_password_email_task

logger = logging.getLogger(__name__)


class UserRegisterView(AtomicMixin, CreateModelMixin, GenericAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = ()

    def post(self, request):
        """User registration view."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.create(request)
            return Response(status=status.HTTP_201_CREATED)
        logger.warning(f"User Register Error {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserConfirmEmailView(AtomicMixin, GenericAPIView):
    serializer_class = None
    authentication_classes = ()

    def get(self, request, activation_key):
        """
        View for confirm email.

        Receive an activation key as parameter and confirm email.
        """
        user = get_object_or_404(User, activation_key=str(activation_key))
        if user.confirm_email():
            return Response(status=status.HTTP_200_OK)

        logger.warning(f"Email confirmation key not found: {activation_key}")
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserEmailConfirmationStatusView(GenericAPIView):
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Retrieve user current confirmed_email status."""
        user = self.request.user
        return Response({"status": user.confirmed_email}, status=status.HTTP_200_OK)


class UserOwnAccountView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"user": self.get_serializer(request.user).data})


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetView(GenericAPIView):
    serializer_class = RequestPasswordResetSerializer
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            send_reset_password_email_task.delay(request.data["email"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    authentication_classes = ()

    def update(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
