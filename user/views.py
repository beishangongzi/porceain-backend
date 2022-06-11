import random
import uuid

import rest_framework.decorators
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method
from django_redis import get_redis_connection
from rest_framework.parsers import JSONParser, MultiPartParser

from utils.tencent.msg import send_msg
from . import serializers
from . import models
from . import schemas
from .auth.auth import JwtQueryParamsAuthentication


class LoginView(APIView):
    authentication_classes = []
    parser_classes = [MultiPartParser, JSONParser]
    @swagger_auto_schema(request_body=serializers.LoginSerializer)
    def post(self, request, *args, **kwargs):
        """
        1. 校验手机号是否合法
        2. 校验验证码， redis
            - 无验证吗
            - 有验证码， 输入错误
            - 有验证码 输入正确

        3. 去数据库获取用户信息
        4. 将信息返回给小程序
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ser = serializers.LoginSerializer(data=request.data)
        is_valid = ser.is_valid(raise_exception=False)
        if not is_valid:
            return Response({"status": False, "message": "验证码错误"})

        phone = ser.validated_data["phone"]
        user_instance, flag = models.User.objects.get_or_create(phone=phone)
        # user_instance.token = str(uuid.uuid4())
        user_instance.save()
        payload = {
            "id": user_instance.id,
            "user_name": user_instance.username
        }
        token = JwtQueryParamsAuthentication().create_token(payload, {"minutes": 3})
        return Response({"status": True, "username": user_instance.get_username(), "token": token})


class LoginWithPassword(APIView):
    authentication_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body=serializers.LoginPassWordSerializer)
    def post(self, request, *args, **kwargs):
        ser = serializers.LoginPassWordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user_instance = models.User.objects.get(phone=ser.validated_data["phone"])
        payload = {
            "id": user_instance.id,
            "user_name": user_instance.username
        }
        token = JwtQueryParamsAuthentication().create_token(payload, {"days": 3})
        return Response({"status": True, "user": user_instance.data, "token": token})


class MessageView(APIView):
    authentication_classes = []
    parser_classes = [MultiPartParser, JSONParser]

    @swagger_auto_schema(request_body=serializers.MessageSerializer, )
    def post(self, request, *args, **kwargs):

        # 获取手机号

        # 手机号校验
        ser = serializers.MessageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        # 生产随机验证码
        code = random.randint(1000, 9999)
        phone = ser.validated_data["phone"]
        print(code)
        conn = get_redis_connection()
        if conn.exists(phone):
            print(f"exist {phone}---{conn.get(phone)}")
            return Response({"status": False, "message": "发送失败!"})
        conn.set(phone, code, ex=100)
        # 验证吗发送到手机上
        flag = send_msg(phone, code)
        # 校对验证

        if flag:
            return Response({"status": True, "message": "发送成功"})
        else:
            return Response({"status": False, "message": "发送失败"})


