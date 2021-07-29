from rest_framework import serializers

from utils import validate_email as email_is_valid

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_email(self, value):
        if not email_is_valid(value):
            raise serializers.ValidationError(
                "Please use a different email address provider."
            )

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already in use, please use a different email address."
            )

        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Wrong password.")
        return value

    def save(self, **kwargs):
        password = self.validated_data["new_password"]
        user = self.context["request"].user
        user.set_password(password)
        user.save()
        return user


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    key = serializers.CharField(max_length=128, required=True)

    def save(self, **kwargs):
        password = self.validated_data["new_password"]
        key = self.validated_data["key"]
        user = User.objects.get(activation_key=key)
        user.set_password(password)
        user.save()
        return user
