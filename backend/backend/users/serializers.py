import django.contrib.auth.password_validation as password_validation
from django.contrib.auth import get_user_model
from django.core import exceptions
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
        )
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        user = User(**attrs)

        password = attrs.get("password", None)

        if password:
            errors = dict()

            try:
                password_validation.validate_password(password=password, user=user)
            except exceptions.ValidationError as e:
                errors["password"] = list(e.messages)

            if errors:
                raise exceptions.ValidationError(errors)

        return super().validate(attrs)
