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
from camus.case import views
from common import app_conf_views

urlpatterns = [
    path('api/v1/', include([
        path('case', views.CaseList.as_view(), name='CaseList'),
        path('caseTemplate', views.CaseTemplate.as_view(), name="CaseTemplate"),
        path('caseFile', views.CaseFile.as_view(), name='CaseFile'),
        path('caseSearch', views.CaseSearch.as_view(), name='CaseSearch'),
        path('case/<int:pk>', views.CaseDetail.as_view(), name='CaseDetail'),
    ]
    ), )
]
