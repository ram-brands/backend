from django.db import transaction

from rest_framework.serializers import CharField, ModelSerializer, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer

from .models import User


class TokenLoginSerializer(TokenObtainSlidingSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "full_name",
            "token",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    token = CharField(read_only=True, required=False)

    @transaction.atomic
    def create(self, validated_data):
        user = super().create(validated_data)
        user.token = TokenLoginSerializer.get_token(user)
        return user

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(**kwargs)

        if "password" in self.validated_data:
            password = self.validated_data["password"]
            user.set_password(password)
            user.save()

        return user

    def validate_password(self, value):
        PASSWORD_MIN_LENGTH = 6

        if len(value) < PASSWORD_MIN_LENGTH:
            raise ValidationError(
                f"Ensure this field has no less than {PASSWORD_MIN_LENGTH} characters."
            )

        return value
