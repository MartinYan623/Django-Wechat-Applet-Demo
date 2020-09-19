from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
import random
from django_redis import get_redis_connection
from api import models
from .serializer.account import MessageSerializer, LoginSerializer


class MessageView(APIView):

    def get(self, request, *args, **kwargs):
        # 1.获取手机号
        # 2.手机格式校验
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status': False, 'message': '手机格式错误'})
        phone = ser.validated_data.get('phone')
        # 3.生成随机验证码
        random_code = random.randint(1000, 9999)
        # 4.验证码发送到手机上，购买服务器进行发送短信：腾讯云
        # 这一步改为将验证码返回显示到前端 让用户手动输入 再到redis匹配
        # 5.把验证码+手机号保留（30s过期）
        print(random_code)

        conn = get_redis_connection()
        conn.set(phone, random_code, ex=60)
        return Response({"status": True, 'message': '发送短信验证码成功'})


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        # 通过serializer实现了对手机号和验证码的校验
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'message': '验证码错误'})
        # 校验成功后需要查询或创建用户
        phone = ser.validated_data.get('phone')
        user_object, flag = models.UserInfo.objects.get_or_create(phone=phone)
        user_object.token = str(uuid.uuid4())
        user_object.save()
        return Response({"status": True, "data": {"token": user_object.token, 'phone': phone}})
