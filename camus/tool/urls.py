#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
=================================================
@Project -> File   ：camus-server -> urls
@IDE    ：PyCharm
@Author ：Lance
@Date   ：2020/3/3 8:56 上午
@Desc   ：check readme.md
==================================================
"""

from django.urls import path, include
from camus.tool import views

urlpatterns = [
    path('api/v1/', include([
        path('idInfo', views.IdInfoDetail.as_view(), name='idInfo'),
        path('idCard', views.IdCardDetil.as_view(), name='idCard'),
        path('dateExtrapolation', views.DateExtrapolated.as_view(), name='dateExtrapolation'),
        path('DateInterval', views.DateInterval.as_view(), name='DateInterval')
    ]
    ), )
]
