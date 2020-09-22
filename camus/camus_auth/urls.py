# -*- coding: utf-8 -*-
# @Time    : 2020-03-07 14:43
# @Author  : Lance
# @File    : urls.py

from django.urls import path, include
from camus.camus_auth import views

urlpatterns = [
    path('api/v1/', include([
        path('user', views.User.as_view(), name='getAllUser'),
        path('auth/login', views.AuthLogin.as_view(), name='login'),
        path('tokenUser', views.TokenUser.as_view(), name='getUserByToken'),
    ]
    ), )
]
