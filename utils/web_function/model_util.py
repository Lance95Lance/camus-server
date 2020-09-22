#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
=================================================
@Project -> File   ：camus-server -> model_utils
@IDE    ：PyCharm
@Author ：Lance
@Date   ：2020/3/18 2:48 下午
@Desc   ：model工具类
==================================================
"""
import logging

from camus.project.models import ProjectDetail, ProjectProgress
from camus.project.serializers import ProjectDetailSerializer, ProjectProgressSerializer, ProjectProgressChangeSerializer

logger = logging.getLogger('camus.common')


class ModelUtil:
    def __init__(self, model_class):
        self.model_class = model_class

    def check_data_exist(self, **kwargs) -> tuple:
        """
        检查数据是否存在:
        存在返回: (True，查询结果query)
        不存在返回: (False, 文案)
        """
        try:
            return True, self.model_class.objects.get(**kwargs)
        except self.model_class.DoesNotExist:
            # 不存在返回False
            return False, '示例不存在'


class ProjectModelUtil:
    def __init__(self):
        pass

    def check_process_stage_and_change_project_status(self, project_detail_id) -> bool:
        """
        检查对应项目的所有项目进度是否已经已上线,如果皆已上线则更改对应项目详情状态，反之则不变更:
        存在返回: (True，查询结果query)
        不存在返回: (False, 文案)
        """

        result = ProjectProgress.objects.filter(project_detail_id=project_detail_id)
        serializer = ProjectProgressSerializer(result, many=True)

        is_finished_flag = True

        for i in serializer.data:
            if i['stage'] != 8:
                is_finished_flag = False

        if is_finished_flag is True:

            logger.info(f"项目详情ID:{project_detail_id} 下的项目进度均已上线,变更状态")

            project_detail_result = ProjectDetail.objects.get(id=project_detail_id)
            serializer = ProjectProgressChangeSerializer(project_detail_result, data={"status": 1})

            if serializer.is_valid():
                serializer.save()

                logger.info(f"变更状态成功")

                return True

            logger.error(f"变更状态失败:{serializer.errors}")
            return False
        else:

            logger.info(f"项目详情ID:{project_detail_id} 下的项目进度未全部上线,变更状态")

            project_detail_result = ProjectDetail.objects.get(id=project_detail_id)
            serializer = ProjectProgressChangeSerializer(project_detail_result, data={"status": 0})

            if serializer.is_valid():
                serializer.save()

                logger.info(f"变更状态成功")

                return True

            logger.error(f"变更状态失败:{serializer.errors}")
            return False
        # try:
        #     return True, self.model_class.objects.get(**kwargs)
        # except self.model_class.DoesNotExist:
        #     # 不存在返回False
        #     return False, '示例不存在'
