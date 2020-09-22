# Create your models here.
from django.db import models
from camus.case.case_enum import CasePriority, CaseStatus


class CaseBase(models.Model):
    """用例基础信息表"""
    project_id = models.BigIntegerField(verbose_name="项目ID")
    case_title = models.CharField(verbose_name="用例标题", max_length=500)
    case_detail = models.TextField(verbose_name="用例详情", null=True)
    case_priority = models.CharField(verbose_name="用例优先级", max_length=10, choices=CasePriority, blank=True)
    case_status = models.CharField(verbose_name="用例状态", max_length=10, choices=CaseStatus, blank=False,
                                   default="NO_EXECUTE")
    case_bug = models.BooleanField(default=False)
    created_person = models.TextField(verbose_name="创建者")
    updated_person = models.TextField(verbose_name="更新者", null=True)
    gmt_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = "case_base"
        ordering = ['gmt_created']
        indexes = [
            models.Index(fields=['case_title'], name='case_base_idx')
        ]


class CaseFile(models.Model):
    """用例文件表"""
    project_id = models.BigIntegerField(verbose_name="项目ID")
    excel_name = models.CharField(verbose_name="文件名", max_length=500)
    excel_alias_name = models.TextField(verbose_name="文件别名")
    upload_person = models.TextField(verbose_name="创建者")
    # case_priority = models.CharField(verbose_name="用例优先级", max_length=10, choices=CasePriority, blank=True)
    # case_status = models.CharField(verbose_name="用例状态", max_length=10, choices=CaseStatus, blank=True)
    # case_bug = models.BooleanField(default=False, blank=True)
    # created_person = models.TextField(verbose_name="创建者")
    gmt_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = "case_file"
        ordering = ['gmt_created']
        indexes = [
            models.Index(fields=['excel_name'], name='case_file_idx')
        ]
