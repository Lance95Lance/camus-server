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
import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from camus.case import case_enum
from camus.project.models import CamusConfig
from camus.project.serializers import CamusConfigSerializer
from utils.web_function.CommonResponse import BaseResponse
from utils.web_function.conf_util import ConfUtil
from utils.other_utils import constant as const

case_priority = ConfUtil(case_enum.CasePriority).get_enum_dict()
case_status = ConfUtil(case_enum.CaseStatus).get_enum_dict()


class AppConf(APIView):
    """配置接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        data = {
            "case_priority": case_priority,
            "case_status": case_status,
            "area_info": const.AREA_INFO,
        }
        conf = CamusConfig.objects.all()
        # searlizer = CamusConfigSerializer(conf, many=True)

        for sql_result in conf:
            for key, value in sql_result.to_json().items():
                data[key] = value

        return Response(BaseResponse(data=data).context())
