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
from camus.case.models import CaseBase, CaseFile


class CaseBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseBase
        fields = '__all__'


class CaseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseFile
        fields = '__all__'

#
# class CaseSearchSerializer(serializers.Serializer):
#     external_order_no = serializers.StringRelatedField()
#     product_code = serializers.IntegerField()
#     t_time = serializers.DateField()
#     run_env = serializers.IntegerField()
#     scene_gather = serializers.JSONField()
#
#     def create(self, validated_data):
#         return CaseBase.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.external_order_no = validated_data.get('external_order_no', instance.external_order_no)
#         instance.product_code = validated_data.get('product_code', instance.product_code)
#         instance.t_time = validated_data.get('t_time', instance.t_time)
#         instance.run_env = validated_data.get('run_env', instance.run_env)
#         instance.scene_gather = validated_data.get('scene_gather', instance.scene_gather)
#         instance.save()
#         return instance
