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
from camus.project import views
from common import app_conf_views

urlpatterns = [
    path('api/v1/', include([
        path('conf', app_conf_views.AppConf.as_view(), name='AppConf'),
        path('area', views.ProjectAreaList.as_view(), name='ProjectAreaList'),
        path('project', views.ProjectList.as_view(), name='ProjectList'),
        path('project/<int:pk>', views.ProjectDetailApi.as_view(), name='ProjectDetailApi'),
        path('projectProgress', views.ProjectProgressList.as_view(), name='ProjectProgressList'),
        path('projectProgress/<int:pk>', views.ProjectProgressDetail.as_view(), name='ProjectProgressDetail'),
        path('projectDashboard', views.ProjectDashboard.as_view(), name='ProjectDashboard'),
        # path('project', views.ModifyProjectDetail.as_view(), name='ModifyProjectDetail'),
        # path('project', views.ProjectList.as_view(), name='projectList'),
        # path('project/<int:pk>', views.ProjectDetail.as_view(), name='projectDetail'),
    ]
    ), )
]
