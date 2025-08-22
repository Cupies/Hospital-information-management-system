from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Count
from .models import (
    User, doctor, patient, department, Registration_type, 
    Drug_information, Drug_inventory, Fee_items, Template, 
    Emr, Outpatient_registration, Outpatient_pricing, Outpatient_details, warehouse
)
import json
import datetime
import random
import logging

# 获取logger实例
logger = logging.getLogger(__name__)

# 通用工具函数
def parse_json_request(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return None

def generate_unique_number(prefix):
    now = datetime.datetime.now()
    random_number = random.randint(100, 999)
    return f"{prefix}_{now.strftime('%Y%m%d%H%M%S')}{random_number}"

# 用户相关视图
@require_http_methods(["POST"])
def register(request):
    data = parse_json_request(request)
    if not data:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)

    username = data.get('username')
    password = data.get('password')
    if User.objects.filter(账号=username).exists():
        return JsonResponse({'error': '账号已存在'}, status=400)

    User.objects.create(账号=username, 密码=password, 权限=0)
    return JsonResponse({'codestatus': 1}, safe=False)

@require_http_methods(["POST"])
def login_view(request):
    data = parse_json_request(request)
    if not data:
        return JsonResponse({'loginstatus': '无效的JSON格式'}, status=400)

    username = data.get('username')
    password = data.get('password')
    try:
        user = User.objects.get(账号=username)
        if user.密码 == password:
            response = {
                'loginstatus': '登录成功',
                '权限': user.权限,
                '需要绑定病人编号': user.权限 == '0' and not user.病人编号,
                '需要绑定医生编号': user.权限 == '2' and not user.医生编号,
                'username': user.账号
            }
            return JsonResponse(response)
        return JsonResponse({'loginstatus': '账号或密码错误'})
    except User.DoesNotExist:
        return JsonResponse({'loginstatus': '账号不存在'})

# 医生相关视图
@csrf_exempt
@require_http_methods(["GET"])
def doctor_list(request):
    doctors = doctor.objects.all().values()
    return JsonResponse(list(doctors), safe=False)

@require_http_methods(["POST"])
def add_doctor(request):
    data = parse_json_request(request)
    if not data:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)

    编号 = data.get('编号')
    if doctor.objects.filter(编号=编号).exists():
        return JsonResponse({'status': '添加失败', 'error': '该编号已存在'}, status=400)

    doctor.objects.create(
        编号=编号,
        姓名=data.get('姓名'),
        性别=data.get('性别'),
        科室=data.get('科室'),
        备注=data.get('备注', '')
    )
    return JsonResponse({'status': '添加成功', 'doctor_id': 编号}, status=201)

# 药品相关视图
@require_http_methods(["POST"])
def add_drug(request):
    data = parse_json_request(request)
    if not data:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)

    编号 = data.get('编号')
    if Drug_information.objects.filter(编号=编号).exists():
        return JsonResponse({'status': '添加失败', 'error': '该药品编号已存在'}, status=400)

    Drug_information.objects.create(
        编号=编号,
        名称=data.get('名称'),
        规格=data.get('规格'),
        整量单位=data.get('整量单位'),
        散量单位=data.get('散量单位'),
        入库单价=data.get('入库单价'),
        出库单价=data.get('出库单价'),
        批发价=data.get('批发价'),
        整散比=data.get('整散比'),
        分类=data.get('分类'),
        费用归类=data.get('费用归类'),
        拼音码=data.get('拼音码'),
        效期=data.get('效期'),
        上限=data.get('上限'),
        下限=data.get('下限')
    )
    return JsonResponse({'status': '添加成功', 'drug_id': 编号}, status=201)

# 病历相关视图
@require_POST
def save_emr(request):
    data = parse_json_request(request)
    if not data:
        return JsonResponse({'message': '无效的JSON格式'}, status=400)

    emr = Emr.objects.create(
        病历编号=generate_unique_number('EMR'),
        病人编号=data.get('病人编号', ''),
        姓名=data.get('姓名', ''),
        性别=data.get('性别', ''),
        年龄=data.get('年龄', ''),
        民族=data.get('民族', ''),
        费用类型=data.get('费用类型', ''),
        电话=data.get('电话', ''),
        医生姓名=data.get('医生姓名', ''),
        挂号科室=data.get('挂号科室', ''),
        主诉=data.get('主诉', ''),
        现病史=data.get('现病史', ''),
        往病史=data.get('往病史', ''),
        诊断=data.get('诊断', '')
    )
    return JsonResponse({'message': '病历保存成功', 'emr_id': emr.病历编号})




