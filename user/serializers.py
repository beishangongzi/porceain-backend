import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models


class MessageSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", required=True)

    def validate(self, attrs):
        print(attrs)
        phone = attrs["phone"]
        if not re.match("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$", phone):
            raise ValidationError(detail="手机号错误", code="phone_error")
        return attrs

def validate_phone(value):
    if not re.match("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$", value):
        raise ValidationError(detail="手机号错误", code="phone_error")
    return value

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", required=True, validators=[validate_phone])
    code = serializers.CharField(label="验证码", required=True)




    def validate_code(self, value):
        if len(value) != 4:
            raise ValidationError(detail="验证码长度错误", code="code_error")
        if not value.isdecimal():
            raise ValidationError(detail="验证码格式错误", code="code_error")

        phone = self.initial_data.get("phone")
        conn = get_redis_connection()
        code = conn.get(phone)
        if not code:
            raise ValidationError(detail="验证码格式错误", code="code_error")

        if value != code.decode("utf-8"):
            raise ValidationError(detail="验证码错误", code="code_error")
        return value


class LoginPassWordSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", required=True, validators=[validate_phone])
    password = serializers.CharField(label="password", required=True)

    def validate(self, attrs):
        try:
            instance = models.User.objects.get(phone=attrs["phone"])
        except:
            raise ValidationError(detail="user does not exists", code="user error")
        print(instance.password)
        print(attrs["password"])
        if attrs["password"] != instance.password:
            raise ValidationError(detail="password does not correct", code="password error", )

        return attrs

class LoginResponseSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号")
    token = serializers.UUIDField(label="token")

