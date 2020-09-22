import logging
import datetime


from django.forms import model_to_dict

# Create your views here.
from rest_framework.views import APIView

from camus.project.models import ProjectArea, ProjectDetail, ProjectProgress
from camus.project.serializers import ProjectDetailSerializer, ProjectProgressSerializer, ProjectAreaSerializer
from utils.web_function.CommonResponse import BaseResponse
from utils.web_function.common_util import CommonUtil
from utils.web_function.model_util import ModelUtil, ProjectModelUtil
from rest_framework.response import Response

logger = logging.getLogger('camus.common')


class ProjectAreaList(APIView):
    """项目域接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        """获取全部项目域"""

        result = ProjectArea.objects.all()
        serializer = ProjectAreaSerializer(result, many=True)

        return Response(BaseResponse(data=serializer.data).context())


class ProjectList(APIView):
    """项目域接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        """获取全部域"""

        result = ProjectDetail.objects.all()
        serializer = ProjectDetailSerializer(result, many=True)

        return Response(BaseResponse(data=serializer.data).context())

    def post(self, request):
        """
        新增项目
        """

        logger.info(f"项目模块 >>>>>> 新增项目,入参：{request.data}")

        if ModelUtil(ProjectArea).check_data_exist(id=request.data['project_area_id'])[0] is False:
            return Response(BaseResponse(code=500, message="无对应项目域id,请检查").context())

        serializer = ProjectDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(BaseResponse().context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())


class ProjectDetailApi(APIView):
    """项目域接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request, pk):
        """获取对应项目域下的所有项目"""

        result = ProjectDetail.objects.filter(project_area_id=pk)

        current_week = CommonUtil().get_current_week()

        query_final_result = []
        for query in result:
            # 放行状态为 0进行中 和 本周内状态为 -1异常 或 1已完成 的项目
            if (query.status == -1 or query.status == 1) and (current_week[0] <= query.gmt_modified.date() <= current_week[1]):
                query_final_result.append(query)
            elif query.status == 0:
                query_final_result.append(query)
            else:
                pass

        serializer = ProjectDetailSerializer(query_final_result, many=True)
        return Response(BaseResponse(data=serializer.data).context())

    def put(self, request, pk):
        """修改对应的项目详情"""

        logger.info(f"项目模块 >>>>>> 修改对应项目,入参：项目ID：{pk}")
        logger.info(f"项目模块 >>>>>> 修改对应项目,入参：{request.data}")

        result = ModelUtil(ProjectDetail).check_data_exist(id=pk)

        if result[0] is False:
            return Response(BaseResponse(code=500, message="无对应项目详情id,请检查").context())

        serializer = ProjectDetailSerializer(result[1], data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(BaseResponse().context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())

    def delete(self, request, pk, format=None):
        """删除对应项目"""

        query_data = ModelUtil(ProjectDetail).check_data_exist(id=pk)

        # 对应项目是否存在检查
        if query_data[0] is False:
            return Response(BaseResponse(code=500, message="对应项目不存在或已删除,请检查").context())

        # query_data[1].delete()

        request.data['status'] = -1
        serializer = ProjectDetailSerializer(query_data[1], data=request.data)
        if serializer.is_valid():
            serializer.save()

            logger.info(f"项目模块 >>>>>> 删除对应项目成功,项目详情：{ProjectDetailSerializer(query_data[1]).data}")

            return Response(BaseResponse().context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())


class ProjectProgressList(APIView):
    def post(self, request):
        """
        新增项目
        """

        logger.info(f"项目进度模块 >>>>>> 新增项目进度,入参：{request.data}")

        if ModelUtil(ProjectDetail).check_data_exist(id=request.data['project_detail_id'])[0] is False:
            return Response(BaseResponse(code=500, message="无对应项目详情id,请检查").context())

        serializer = ProjectProgressSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            ProjectModelUtil().check_process_stage_and_change_project_status(request.data['project_detail_id'])

            return Response(BaseResponse().context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())


class ProjectProgressDetail(APIView):
    """项目进度接口"""

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request, pk):
        """获取对应项目详情下的所有项目进度"""

        result = ProjectProgress.objects.filter(project_detail_id=pk)
        serializer = ProjectProgressSerializer(result, many=True)
        return Response(BaseResponse(data=serializer.data).context())

    def put(self, request, pk):
        """修改对应项目进度"""

        logger.info(f"项目进度模块 >>>>>> 修改对应项目进度,入参：项目ID：{pk}")
        logger.info(f"项目进度模块 >>>>>> 修改对应项目进度,入参：{request.data}")

        result = ModelUtil(ProjectProgress).check_data_exist(id=pk)

        if result[0] is False:
            return Response(BaseResponse(code=500, message="无对应项目进度id,请检查").context())

        serializer = ProjectProgressSerializer(result[1], data=request.data)
        if serializer.is_valid():
            serializer.save()
            ProjectModelUtil().check_process_stage_and_change_project_status(request.data['project_detail_id'])
            return Response(BaseResponse().context())
        return Response(BaseResponse(code=500, message=serializer.errors).context())

    def delete(self, request, pk, format=None):
        """删除对应项目"""

        query_data = ModelUtil(ProjectProgress).check_data_exist(id=pk)

        # 对应项目是否存在检查
        if query_data[0] is False:
            return Response(BaseResponse(code=500, message="对应项目进度不存在或已删除,请检查").context())
        else:
            project_detail_id = ProjectProgressSerializer(query_data[1], many=False).data['project_detail_id']

        query_data[1].delete()

        logger.info(f"项目进度模块 >>>>>> 删除对应项目进度成功,项目详情：{ProjectProgressSerializer(query_data[1]).data}")

        ProjectModelUtil().check_process_stage_and_change_project_status(
            project_detail_id
        )

        return Response(BaseResponse().context())


class ProjectDashboard(APIView):

    # permission_classes = (IsAuthenticated,)  # 权限管控

    def get(self, request):
        """获取项目进度看板数据"""

        start_date, end_date = request.GET.get("start_date", None), request.GET.get("end_date", None)

        # 使用date查询需要多+1天，否则会漏掉最后一天的数据
        end_date = (datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        bi_data = []

        # 三维数组
        # 先获取项目域
        project_areas = ProjectArea.objects.all()
        for project_area in project_areas:
            project_area_name = project_area.name
            project_area_id = project_area.id

            projects_result = []

            # 获取时间段内的项目详情
            project_details = ProjectDetail.objects.filter(project_area_id=project_area_id,
                                                           gmt_modified__range=(start_date, end_date))

            for project_detail in project_details:
                project_detail_name = project_detail.name
                project_detail_id = project_detail.id

                project_process_result = []

                project_process_s = ProjectProgress.objects.filter(
                    project_detail_id=project_detail_id,
                    gmt_modified__range=(start_date, end_date)
                )

                for project_process in project_process_s:
                    project_process_result.append(model_to_dict(project_process))

                if project_process_result:
                    project_dict = {'name': project_detail_name, 'monitors': project_process_result}
                    projects_result.append(project_dict)

            if projects_result:
                ares_result = {'name': project_area_name, 'projects': projects_result}
                bi_data.append(ares_result)

        return Response(BaseResponse(data=bi_data).context())

#
# class ProjectList(APIView):
#     """项目接口"""
#
#     # permission_classes = (IsAuthenticated,)  # 权限管控
#
#     def get(self, request):
#         """
#         获取全部项目
#         :param request:
#         :return: Response
#         """
#         # query_data = ProjectBase.objects.all()
#         # serializer = ProjectBaseSerializer(query_data, many=True)
#
#         # 聚合查询
#         result = ProjectBase.objects.raw(selectProjectWithCaseCount)
#         serializer = ProjectBaseJoinCaseSerializer(result, many=True)
#
#         return Response(BaseResponse(data=serializer.data).context())
#
#     def post(self, request):
#         """
#         新增项目
#         :param request:
#         :return: Response
#         """
#
#         logger.info(f"用例模块 >>>>>> 新增项目接口,入参：{request.data}")
#
#         serializer = ProjectBaseSerializer(data=request.data)
#
#         # 重复项检查
#         if ModelUtil(ProjectBase).check_data_exist(
#                 project_title=request.data['project_title'])[0] is True:
#             return Response(BaseResponse(code=500, message="项目名重复,请检查").context())
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(BaseResponse().context())
#         return Response(BaseResponse(code=500, message=serializer.errors).context())

# class ProjectDetail(APIView):
#
#     # permission_classes = (IsAuthenticated,)  # 权限管控
#
#     def put(self, request, pk, format=None):
#         """
#         修改对应项目
#         :param request:
#         :param pk:
#         :param format:
#         :return:
#         """
#         logger.info(f"用例模块 >>>>>> 修改对应项目,入参：项目ID：{pk}")
#         logger.info(f"用例模块 >>>>>> 修改对应项目,入参：{request.data}")
#
#         if request.data.get("updated_person", None) is None or "":
#             return Response(BaseResponse(code=500, message="更新者必填").context())
#
#         query_data = ModelUtil(ProjectBase).check_data_exist(id=pk)
#
#         # 关联项目是否存在检查
#         if query_data[0] is False:
#             return Response(BaseResponse(code=500, message="对应项目不存在或已删除,请检查").context())
#
#         # # 重复项检查
#         # if query_data[0] is True:
#         #     return Response(BaseResponse(code=500, message="项目名重复,请检查").context())
#
#         serializer = ProjectBaseSerializer(query_data[1], data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(BaseResponse().context())
#         return Response(BaseResponse(code=500, message=serializer.errors).context())

# def delete(self, request, pk, format=None):
#     """删除对应项目"""
#
#     query_data = ModelUtil(ProjectBase).check_data_exist(id=pk)
#
#     # 对应项目是否存在检查
#     if query_data[0] is False:
#         return Response(BaseResponse(code=500, message="对应项目不存在或已删除,请检查").context())
#
#     query_data[1].delete()
#
#     logger.info(f"用例模块 >>>>>> 删除对应项目成功,项目详情：{ProjectBaseSerializer(query_data[1]).data}")
#
#     return Response(BaseResponse().context())
