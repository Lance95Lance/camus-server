import logging
import datetime

# Create your views here.
from random import random

from rest_framework.views import APIView

from camus.tool.enity import IdNumberEnity
from camus.tool.serializers import IdNumberSerializer
from utils.other_utils.id_card_util import IdCardUtil
from utils.other_utils.third_party_util import IdNumber
from utils.web_function.CommonResponse import BaseResponse
from rest_framework.response import Response

# Create your views here.
from utils.web_function.common_util import CommonUtil


class IdInfoDetail(APIView):
    """
    身份证工具相关接口
    """

    def get(self, request):
        id_number = request.query_params['idNumber']

        if len(id_number) != 15 and len(id_number) != 18:
            return Response(BaseResponse(code=400, message='身份证号码位数至少15位或18位!').context())

        serializer = IdNumberSerializer(IdNumberEnity(id=id_number))

        return Response(BaseResponse(data=serializer.data).context())

    def post(self, request):
        age = request.data.get('age', 18)
        sex = request.data.get('sex', 0)
        area_id = request.data.get('area_id', None)

        age = int(age)
        sex = int(sex)

        if age == '' or sex == '':
            return Response(BaseResponse(code=400, message='年龄或性别不能为空!').context())

        if age > 500:
            return Response(BaseResponse(code=400, message='最大500岁哦').context())

        return Response(BaseResponse(data=IdNumber.generate_id(sex=sex, age=age, area_id=area_id)).context())


class IdCardDetil(APIView):
    """身份证图片生成接口"""

    def get(self, request):
        id_number = request.query_params['idNumber']

        if len(id_number) != 15 and len(id_number) != 18:
            return Response(BaseResponse(code=400, message='身份证号码位数至少15位或18位!').context())

        serializer = IdNumberSerializer(IdNumberEnity(id=id_number))

        id_info = serializer.data
        print(serializer.data)

        if id_info['facticity'] == '无效':
            return Response(BaseResponse(code=400, message='身份证无效,请检查!').context())

        birth = id_info['birthday'].split('-')
        age = id_info['age']

        # 有效期判断
        # if 16 <= age <= 25:
        #     effect_age = 10
        # elif 26 <= age <= 45:
        #     effect_age = 20
        # else:
        #     effect_age = 100

        image_path = IdCardUtil().generator(
            name='张三',
            sex=id_info['sex'],
            nation='汉',
            year=birth[0],
            mon=birth[1],
            day=birth[2],
            addr=id_info['area_name'] + '大世界街287号',
            idn=id_number,
            org=id_info['area_name'],
            life=birth[0] +
                 '.' +
                 birth[1] +
                 '.' +
                 birth[2] +
                 '-' +
                 str(int(birth[0]) + 40) +
                 '.' +
                 birth[1] +
                 '.' +
                 birth[2],
        )
        if image_path[0]:
            return Response(BaseResponse(data=f'http://XX.XX.XX.XX:4396/image/{image_path[1]}').context())
        else:
            return Response(BaseResponse(code=400, message='身份证图片生成失败').context())


class DateExtrapolated(APIView):

    def get(self, request):
        """date推算接口"""
        date = request.query_params['date']
        days = request.query_params['days']
        if date is None or date == 'Invalid Date':
            return Response(BaseResponse(code=400, message='基础日期不能为空!').context())
        if days is None or days == 'NaN':
            return Response(BaseResponse(code=400, message='天数不能为空!').context())

        data = CommonUtil().get_date_extrapolation(date, int(days))

        return Response(BaseResponse(data=data).context())


class DateInterval(APIView):

    def get(self, request):
        """两个日期相差时间天数计算接口"""
        begin_date = request.query_params['begin_date']
        end_date = request.query_params['end_date']
        if begin_date is None or begin_date == 'Invalid Date':
            return Response(BaseResponse(code=400, message='开始时间不能为空!').context())
        if end_date is None or end_date == 'Invalid Date':
            return Response(BaseResponse(code=400, message='结束时间不能为空!').context())

        data = CommonUtil().get_date_interval(begin_date, end_date)

        return Response(BaseResponse(data=data).context())
