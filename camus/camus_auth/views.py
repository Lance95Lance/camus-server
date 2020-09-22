from django.shortcuts import render

# Create your views here.


import logging
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.web_function.CommonResponse import BaseResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User as UserModel
from camus.camus_auth.serializers import UserSerializer

logger = logging.getLogger('camus.common')


class User(APIView):
    """获取全部用户信息接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        query_data = UserModel.objects.all()
        serializer = UserSerializer(query_data, many=True)
        return Response(BaseResponse(data=serializer.data).context())


class AuthLogin(APIView):
    """登录接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        logger.info(">>>登录接口")

        username = request.successful_authenticator.get_user(
            request.successful_authenticator.get_validated_token(
                request.successful_authenticator.get_raw_token(request.successful_authenticator.get_header(request))))

        return Response(BaseResponse(data=str(username)).context())


class TokenUser(APIView):
    """获取用户信息接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        logger.info(">>>获取用户信息接口")

        username = request.successful_authenticator.get_user(
            request.successful_authenticator.get_validated_token(
                request.successful_authenticator.get_raw_token(request.successful_authenticator.get_header(request))))

        return Response(BaseResponse(data=str(username)).context())
