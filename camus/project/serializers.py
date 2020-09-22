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

from rest_framework import serializers
from camus.project.models import ProjectArea, ProjectDetail, CamusConfig, ProjectProgress


class ProjectAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectArea
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = '__all__'


class CamusConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CamusConfig
        fields = '__all__'


class ProjectProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProgress
        fields = '__all__'


class ProjectProgressChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProgress
        fields = ['status']


# class ProjectBaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectBase
#         fields = '__all__'
#
#
# class ProjectBaseJoinCaseSerializer(serializers.ModelSerializer):
#     case_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ProjectBase
#         fields = ['id', 'project_title', 'project_detail', 'created_person', 'updated_person', 'case_count']
#
#     def get_case_count(self, obj):
#         return obj.case_count
