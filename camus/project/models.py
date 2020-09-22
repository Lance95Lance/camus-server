import json

from django.db import models


# Create your models here.
class ProjectArea(models.Model):
    """
    项目所属域
    """
    name = models.CharField(verbose_name="项目域名称", unique=True, max_length=200)
    description = models.CharField(verbose_name="项目域描述", max_length=500, null=True)
    remark = models.CharField(verbose_name="备注", max_length=64, null=True)
    gmt_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = "project_area"
        ordering = ['gmt_created']

        indexes = [
            models.Index(fields=['name'], name='project_area_idx')
        ]


class ProjectDetail(models.Model):
    """项目详情"""
    project_area_id = models.BigIntegerField(verbose_name="项目域id")
    name = models.CharField(verbose_name="项目名称", max_length=200)
    description = models.CharField(verbose_name="项目描述", max_length=500, null=True)
    status = models.IntegerField(verbose_name="项目状态", default=0)
    created_person = models.TextField(verbose_name="创建者")
    updated_person = models.TextField(verbose_name="更新者", null=True)
    gmt_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = "project_detail"
        ordering = ['gmt_created']

        indexes = [
            models.Index(fields=['name'], name='project_detail_idx')
        ]


class ProjectProgress(models.Model):
    """项目进度"""
    project_detail_id = models.BigIntegerField(verbose_name="项目详情id")
    app_name = models.IntegerField(verbose_name="涉及应用", null=True)
    stage = models.IntegerField(verbose_name="项目阶段", null=True)
    work_time = models.CharField(verbose_name="工作量", max_length=64, null=True)
    outputs = models.CharField(verbose_name="产出", max_length=64, null=True)
    to_measure_time = models.DateField(verbose_name="提测时间", null=True)
    plan_to_prod_time = models.DateField(verbose_name="计划上线", null=True)
    to_prod_time = models.DateField(verbose_name="实际上线", null=True)
    qa_owner = models.CharField(verbose_name="测试负责人", max_length=64, null=True)
    risk_analysis = models.TextField(verbose_name="风险分析", null=True)
    remark = models.TextField(verbose_name="备注", null=True)
    status = models.IntegerField(verbose_name="进度状态", default=0)
    gmt_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = "project_progress"
        ordering = ['gmt_created']


class CamusConfig(models.Model):
    """监控配置表"""
    c_key = models.CharField(verbose_name="配置项键", unique=True, max_length=64)
    c_value = models.TextField(verbose_name="配置项值")
    remark = models.CharField(verbose_name="备注", max_length=64, null=True)
    gmt_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def to_json(self):
        json_md = {
            self.c_key: self.c_value
        }
        return json_md

    class Meta:
        db_table = "camus_config"
        ordering = ['gmt_created']

        indexes = [
            models.Index(fields=['c_key'], name='camus_config_idx')
        ]


# class ProjectBase(models.Model):
#     """项目基础信息表，待完善"""
#     project_title = models.CharField(verbose_name="项目名", unique=True, max_length=200)
#     project_detail = models.TextField(verbose_name="项目详情", blank=True)
#     created_person = models.TextField(verbose_name="创建者")
#     updated_person = models.TextField(verbose_name="更新者", blank=True)
#     gmt_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
#     gmt_modified = models.DateTimeField(verbose_name='修改时间', auto_now=True)
#
#     class Meta:
#         db_table = "project_base"
#         ordering = ['gmt_created']
#
#         indexes = [
#             models.Index(fields=['project_title'], name='project_base_idx')
#         ]
