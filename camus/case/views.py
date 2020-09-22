import json
import logging

# Create your views here.
import os
from datetime import datetime
from random import randint

from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from camus.case.case_enum import CasePriority, CaseStatus
from camus.settings import base
from utils.other_utils.excel_utils import ExcelUtils
from utils.rewrite_utils.MyChoiceEnum import MyChoiceEnumUtil
from utils.web_function.CommonResponse import BaseResponse
from camus.case.serializers import CaseBaseSerializer, CaseFileSerializer
from camus.case.models import CaseBase
from camus.project.models import ProjectDetail
from utils.web_function.model_util import ModelUtil

logger = logging.getLogger('camus.common')


class CaseList(APIView):
    """用例接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        """
        获取全部用例
        """
        case_base_data = CaseBase.objects.all()
        serializer = CaseBaseSerializer(case_base_data, many=True)
        return Response(BaseResponse(data=serializer.data).context())

    def post(self, request):
        """
        新增用例
        """

        logger.info(f"用例模块 >>>>>> 新增用例接口,入参：{request.data}")

        if ModelUtil(ProjectDetail).check_data_exist(id=request.data['project_id'])[0] is False:
            return Response(BaseResponse(code=500, message="无对应项目id,请检查").context())

        # if ModelUtil(CaseBase).check_data_exist(project_id=request.data['project_id'],
        #                                         case_title=request.data['case_title'])[0] is True:
        #     return Response(BaseResponse(code=500, message="所属项目用例标题重复,请检查").context())

        serializer = CaseBaseSerializer(data=request.data)

        # 关联项目是否存在检查
        # if self._check_project_id(request.data['project_id']) is True:
        #     return Response(BaseResponse(data=500, message="无对应项目id,请检查").context())

        if serializer.is_valid():
            serializer.save()
            return Response(BaseResponse().context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())


class CaseDetail(APIView):
    """用例详情接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request, pk, format=None):
        """
        获取对应用例信息
        :param request:
        :param pk:
        :param format:
        :return:
        """
        query_data = ModelUtil(CaseBase).check_data_exist(id=pk)

        if query_data[0] is False:
            return Response(BaseResponse(code=500, message="对应用例不存在,请检查").context())

        serializer = CaseBaseSerializer(query_data[1])
        return Response(BaseResponse(data=serializer.data).context())

    def put(self, request, pk, format=None):
        """
        修改对应用例
        :param request:
        :param pk:
        :param format:
        :return:
        """
        logger.info(f"用例模块 >>>>>> 修改对应用例,入参：用例ID：{pk}")
        logger.info(f"用例模块 >>>>>> 修改对应用例,入参：{request.data}")

        if request.data.get("updated_person", None) is None or "":
            return Response(BaseResponse(code=500, message="更新者必填").context())

        # 关联项目是否存在检查
        if ModelUtil(ProjectDetail).check_data_exist(id=request.data['project_id'])[0] is False:
            return Response(BaseResponse(code=500, message="无对应项目id,请检查").context())

        # 检查对应用例是否存在
        query_data = ModelUtil(CaseBase).check_data_exist(id=pk)

        if query_data[0] is False:
            return Response(BaseResponse(code=500, message="对应用例不存在,请检查").context())

        serializer = CaseBaseSerializer(query_data[1], data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(BaseResponse().context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())

    def delete(self, request, pk, format=None):
        """
        删除对应用例
        :param request:
        :param pk:
        :param format:
        :return:
        """
        logger.info(f"用例模块 >>>>>> 删除对应用例,入参 用例ID：{pk}")

        query_data = ModelUtil(CaseBase).check_data_exist(id=pk)

        if query_data[0] is False:
            return Response(BaseResponse(code=500, message="对应用例不存在,请刷新").context())

        query_data[1].delete()

        logger.info(f"用例模块 >>>>>> 删除对应用例,用例详情：{CaseBaseSerializer(query_data[1]).data}")

        return Response(BaseResponse().context())


class CaseSearch(APIView):

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def post(self, request):
        """条件查询对应用例"""
        logger.info(f"用例模块 >>>>>> 多条件查询,入参：{request.data}")

        # **：解开dict,还原成a=1的形式传入filter
        query_data = CaseBase.objects.filter(**request.data).order_by("id")

        # 前端分页,后端不分页
        serializer = CaseBaseSerializer(query_data, many=True)
        return Response(BaseResponse(data=serializer.data).context())

        # 后端分页
        # mpp = MyPageNumberPagination()
        # page_query_data = mpp.paginate_queryset(queryset=query_data, request=request, view=self)
        #
        # serializer = CaseBaseSerializer(page_query_data, many=True)
        #
        # return Response(PageResponse(
        #     entries=serializer.data,
        #     current=request.query_params.get('pageNum', 2),
        #     pageSize=len(serializer.data),
        #     totalRecords=len(query_data),
        # ).context())


class CaseFile(APIView):

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def post(self, request):
        """文件上传excel进行解析"""
        file = request.FILES.get("file", None)

        request_body = {
            "project_id": request.POST.get('project_id', None),
            "excel_name": None,
            "excel_alias_name": None,
            "upload_person": request.POST.get('upload_person', None)
        }
        if request_body["project_id"] is None or "":
            return Response(BaseResponse(code=500, message="项目id必传").context())

        if request_body["upload_person"] is None or "":
            return Response(BaseResponse(code=500, message="创建人必传").context())

        if file is None or "":
            return Response(BaseResponse(code=500, message="请上传对应文件").context())

        # 关联项目是否存在检查
        if ModelUtil(ProjectDetail).check_data_exist(id=request.data['project_id'])[0] is False:
            return Response(BaseResponse(code=500, message="无对应项目id,请检查").context())

        # 分割文件名和文件后缀
        upload_excel_name = file.name.split('.')
        upload_excel_suffix = ""

        if file:
            # 获取后缀名
            upload_excel_suffix = upload_excel_name[-1].replace("\"", "")
            # 如果上传图片的后缀名不在配置的后缀名里返回格式不允许
            if upload_excel_suffix not in base.ALLOWED_EXCEL_TYPE:
                return Response(BaseResponse(code=500, message="文件格式不对,请检查").context())

        logger.info(f"用例模块 >>>>>> 文件上传,入参：{request_body}")

        # 转换文件名
        excel_alias_name = datetime.now().strftime('%Y%m%d%H%M%S') + str(
            randint(10000, 99999)) + '.' + upload_excel_suffix  # 采用时间和随机数
        path = os.path.join(base.FILES_DIR, excel_alias_name)

        # 文件写入服务器
        with open(path, 'wb') as f:  # 二进制写入
            for i in file.chunks():
                f.write(i)

        # 读取excel
        excel_data = ExcelUtils(path).read_excel()

        logger.info(f"excel总条数: {len(excel_data)}")

        request_body["excel_name"] = upload_excel_name[0]
        request_body["excel_alias_name"] = excel_alias_name

        # 写入用例档,待完善

        case_mode_data = []
        serializer_failed_count = 0

        # 将解析出的excel数据拼装后序列化

        # 数据拼装
        for excel_info in excel_data:
            case_mode_data_dict_temp = {
                "project_id": int(request_body["project_id"]),
                "case_title": excel_info["用例标题"] if excel_info["用例标题"] is not None and excel_info["用例标题"] != "" else
                excel_info["用例详情"],
                "case_detail": excel_info["用例详情"],
                "case_status": MyChoiceEnumUtil(
                    CaseStatus
                ).get_key_from_enum_value(excel_info["用例状态"]) or "NO_EXECUTE",
                "case_bug": False,
                "created_person": request_body["upload_person"],
            }
            if excel_info["用例等级"] is None or "":
                pass
            else:
                case_mode_data_dict_temp["case_priority"] = MyChoiceEnumUtil(
                    CasePriority
                ).get_key_from_enum_value(
                    excel_info["用例等级"])
            # 序列化
            case_base_serializer = CaseBaseSerializer(data=case_mode_data_dict_temp)

            if case_base_serializer.is_valid():
                case_mode_data.append(CaseBase(**case_base_serializer.data))
            else:
                serializer_failed_count += 1
                logger.error(f"用例模块 >>>>>> 序列化失败 {case_base_serializer.errors}")

        try:

            # 批量写入表中
            CaseBase.objects.bulk_create(case_mode_data)
        except Exception as e:
            logger.error(repr(e))
            return Response(BaseResponse(code=500, message=repr(e)).context())

        serializer = CaseFileSerializer(data=request_body)

        if serializer.is_valid():
            serializer.save()
            return Response(
                BaseResponse(data={
                    "file_path": path,
                    "import_detail": f"导入成功 {len(excel_data) - serializer_failed_count} 条,"
                                     f"导入失败 {serializer_failed_count} 条"
                }).context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())


class CaseTemplate(APIView):

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        """获取测试用例模板"""
        template_path = os.path.join(os.path.join(base.BASE_DIR, "resources"), "caseTemplate.xlsx")
        file = open(template_path, 'rb')

        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="caseTemplate.xlsx"'

        return response
