from django.shortcuts import render
from myapp.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
# 注册
#from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)#翻译json为url
        username = data.get('username')  # 从表单获取用户名
        password =data.get('password')  # 从表单获取密码
        # 检查用户名是否已存在
        if User.objects.filter(账号=username).exists():
            return JsonResponse({'error': '账号已存在'}, status=400)
        # 创建并保存新用户，确保密码是加密的
        user = User(账号=username, 密码=password,权限=0)
        user.save()
        return JsonResponse({'codestatus': 1}, safe=False)
    else:
        # 如果不是 POST 请求，可以返回错误或注册表单
        return JsonResponse({'error': '请求方法不支持'}, status=400)

#登陆
# from django.contrib.auth.hashers import check_password
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(账号=username)
            if user.密码 == password:
                # 初始化绑定状态标志
                needs_binding_patient_number = False
                needs_binding_doctor_number = False

                # 检查用户角色并确定是否需要绑定编号
                if user.权限 == '0' and not user.病人编号:  # 病人
                    needs_binding_patient_number = True
                elif user.权限 == '2' and not user.医生编号:  # 医生
                    needs_binding_doctor_number = True

                login_response = {
                    'loginstatus': '登录成功',
                    '权限': user.权限,
                    '需要绑定病人编号': needs_binding_patient_number,
                    '需要绑定医生编号': needs_binding_doctor_number,
                    'username': user.账号
                }
                return JsonResponse(login_response)
            else:
                return JsonResponse({'loginstatus': '账号或密码错误'})
        except User.DoesNotExist:
            return JsonResponse({'loginstatus': '账号不存在'})
    return JsonResponse({'loginstatus': '请通过POST请求登录'})
#登陆弹窗

def bind_number_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    number = data.get('number')
    user_type = data.get('type')

    try:
        user = User.objects.get(账号=username)

        # 验证编号是否存在于patient或doctor表中
        if user_type == 'patient':
            if patient.objects.filter(编号=number).exists():
                user.病人编号 = number  # 更新User模型中的病人编号字段
                user.save()
            else:
                return JsonResponse({'status': '无效的病人编号'})
        elif user_type == 'doctor':
            if doctor.objects.filter(编号=number).exists():
                user.医生编号 = number  # 更新User模型中的医生编号字段
                user.save()
            else:
                return JsonResponse({'status': '无效的医生编号'})

        return JsonResponse({'status': '绑定成功'})
    except User.DoesNotExist:
        return JsonResponse({'status': '用户不存在'})
    except Exception as e:
        # 异常处理
        return JsonResponse({'status': '错误', 'message': str(e)})

from .models import doctor
from django.views.decorators.csrf import csrf_exempt
import json
#doctor显示表格
@csrf_exempt
def doctor_list(request):
    if request.method == 'GET':
        doctors = doctor.objects.all().values()
        return JsonResponse(list(doctors), safe=False)

#doctor添加
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import doctor  
import json

@require_http_methods(["POST"])  # 确保只有POST请求被接受
def add_doctor(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        # 首先检查医生是否已存在
        编号 = data.get('编号')
        if doctor.objects.filter(编号=编号).exists():
            return JsonResponse({'status': '添加失败', 'error': '该编号已存在'}, status=400)

        # 医生不存在，创建新记录
        new_doctor = doctor.objects.create(
            编号=编号,
            姓名=data.get('姓名'),
            性别=data.get('性别'),
            科室=data.get('科室'),
            备注=data.get('备注', '')
        )

        # 如果执行到这里，说明创建成功
        return JsonResponse({'status': '添加成功', 'doctor_id': new_doctor.编号}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '添加失败', 'error': str(e)}, status=500)
#批量删除
from django.views.decorators.http import require_http_methods
from .models import doctor  
import json

@require_http_methods(["POST"])
def batch_delete(request):
    try:
        # 解析请求体中的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))
        ids_to_delete = data.get('ids', [])  # 获取要删除的编号列表

        # 执行批量删除
        doctor.objects.filter(编号__in=ids_to_delete).delete()

        return JsonResponse({'status': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': '删除失败', 'error': str(e)}, status=500)

#获取科室
from .models import department
def get_departments(request):
    departments = department.objects.values_list('名称', flat=True).distinct()
    return JsonResponse(list(departments), safe=False)

#获取备注                     
from .models import Registration_type
def get_registrationTypes(request):
    if request.method == 'GET':
        registration_types = Registration_type.objects.all().values('挂号类型')
        registration_types_list = list(registration_types)
        print(registration_types_list)
        return JsonResponse({'registration_types': registration_types_list})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

#doctor编辑
from django.views.decorators.http import require_http_methods
from .models import doctor
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_http_methods(["POST"])  # 或者 PUT，取决于你的API设计
def update_doctor(request, doctor_id):
    try:
        # 检查请求体是否有内容
        print(request.body)
        if not request.body:
            return JsonResponse({'status': '请求体为空'}, status=400)

        # 尝试解析JSON数据
        data = json.loads(request.body.decode('utf-8'))  # 确保正确解码
       
        doctor_instance = doctor.objects.get(编号=doctor_id)  # 获取特定的 doctor 实例
        doctor_instance.姓名 = data.get('姓名', doctor_instance.姓名)
        doctor_instance.性别 = data.get('性别', doctor_instance.性别)
        doctor_instance.科室 = data.get('科室', doctor_instance.科室)
        doctor_instance.备注 = data.get('备注', doctor_instance.备注)
        doctor_instance.save()
        return JsonResponse({'status': '编辑成功'})
    except doctor.DoesNotExist:
        return JsonResponse({'status': '医生不存在'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '编辑失败', 'error': str(e)}, status=500)
    
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import patient
import json

@require_http_methods(["POST"])
def add_patient(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        编号 = data.get('编号')

        # 检查病人是否已存在
        if patient.objects.filter(编号=编号).exists():
            return JsonResponse({'status': '添加失败', 'error': '该编号已存在'}, status=400)

        # 添加新的病人信息
        new_patient = patient.objects.create(
            编号=编号,
            姓名=data.get('姓名'),
            性别=data.get('性别'),
            年龄=data.get('年龄'),
            民族=data.get('民族'),
            费用类型=data.get('费用类型'),
            电话=data.get('电话'),
            拼音码=data.get('拼音码')
        )

        return JsonResponse({'status': '添加成功', 'patient_id': new_patient.编号}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '添加失败', 'error': str(e)}, status=500)

@require_http_methods(["POST"])
def update_patient(request, patient_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            pat = patient.objects.get(编号=patient_id)
            pat.姓名 = data.get('姓名', pat.姓名)
            pat.性别 = data.get('性别', pat.性别)
            pat.年龄 = data.get('年龄', pat.年龄)
            pat.民族 = data.get('民族', pat.民族)
            pat.费用类型 = data.get('费用类型', pat.费用类型)
            pat.电话 = data.get('电话', pat.电话)
            pat.拼音码 = data.get('拼音码', pat.拼音码)
            pat.save()

            return JsonResponse({'status': '更新成功', 'patient_id': pat.编号}, status=200)

        except patient.DoesNotExist:
            return JsonResponse({'status': '更新失败', 'error': '病人不存在'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'status': '更新失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '更新失败', 'error': str(e)}, status=500)

def get_patients(request):
    try:
        # 获取病人信息列表
        patients = patient.objects.all().values('编号', '姓名', '性别', '年龄', '民族', '费用类型', '电话')
        # 将QuerySet转换为列表，因为QuerySet不是JSON可序列化的
        patients_list = list(patients)
        return JsonResponse(patients_list, safe=False)  # 设置safe=False以允许非字典对象
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@require_http_methods(["POST"])
def batch_delete_patients(request):
    try:
        # 解析请求体中的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))
        ids_to_delete = data.get('ids', [])  # 获取要删除的病人编号列表

        if not ids_to_delete:
            return JsonResponse({'status': '删除失败', 'error': '未提供要删除的病人编号'}, status=400)

        # 执行批量删除
        delete_count, _ = patient.objects.filter(编号__in=ids_to_delete).delete()

        return JsonResponse({'status': '删除成功', 'deleted_count': delete_count})
    except json.JSONDecodeError:
        return JsonResponse({'status': '删除失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '删除失败', 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_patient_info(request, patient_id):
    try:
        new_patient = patient.objects.get(编号=patient_id)
        # 将病人信息转换为JSON格式返回
        patient_info = {
            "编号": new_patient.编号,
            "姓名": new_patient.姓名,
            "性别": new_patient.性别,
            "年龄": new_patient.年龄,
            "民族": new_patient.民族,
            "费用类型": new_patient.费用类型,
            "电话": new_patient.电话,
            "拼音码": new_patient.拼音码
        }
        return JsonResponse(patient_info)
    except patient.DoesNotExist:
        return JsonResponse({"error": "病人不存在"}, status=404)
    
@require_http_methods(["GET"])
def get_patient_id(request):
    try:
        username = request.GET.get('username')
        patient_instance = User.objects.get(账号=username)
        return JsonResponse({"patientId": patient_instance.病人编号})
    except User.DoesNotExist:
        return JsonResponse({"error": "病人不存在"}, status=404)
    
@require_http_methods(["PATCH"])
def update_patient_info(request, patient_id):
    try:
        new_patient = patient.objects.get(编号=patient_id)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(new_patient, key, value)
        new_patient.save()
        return JsonResponse({"message": "病人信息已更新"})
    except patient.DoesNotExist:
        return JsonResponse({"error": "病人不存在"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

from .models import Drug_information

def get_drugs(request):
    try:
        drugs = Drug_information.objects.all().values()
        return JsonResponse(list(drugs), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@require_http_methods(["POST"])
def add_drug(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        drug_id = data.get('编号')

        # 检查药品是否已存在
        if Drug_information.objects.filter(编号=drug_id).exists():
            return JsonResponse({'status': '添加失败', 'error': '该药品编号已存在'}, status=400)

        # 添加新的药品信息
        new_drug = Drug_information.objects.create(
            编号=drug_id,
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

        return JsonResponse({'status': '添加成功', 'drug_id': new_drug.编号}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '添加失败', 'error': str(e)}, status=500)

@require_http_methods(["POST"])
def update_drug(request, drug_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            drug = Drug_information.objects.get(编号=drug_id)
            drug.名称 = data.get('名称', drug.名称)
            drug.规格 = data.get('规格', drug.规格)
            drug.整量单位 = data.get('整量单位', drug.整量单位)
            drug.散量单位 = data.get('散量单位', drug.散量单位)
            drug.入库单价 = data.get('入库单价', drug.入库单价)
            drug.出库单价 = data.get('出库单价', drug.出库单价)
            drug.批发价 = data.get('批发价', drug.批发价)
            drug.整散比 = data.get('整散比', drug.整散比)
            drug.分类 = data.get('分类', drug.分类)
            drug.费用归类 = data.get('费用归类', drug.费用归类)
            drug.拼音码 = data.get('拼音码', drug.拼音码)
            drug.效期 = data.get('效期', drug.效期)
            drug.上限 = data.get('上限', drug.上限)
            drug.下限 = data.get('下限', drug.下限)
            drug.save()

            return JsonResponse({'status': '更新成功', 'drug_id': drug.编号}, status=200)

        except Drug_information.DoesNotExist:
            return JsonResponse({'status': '更新失败', 'error': '药品不存在'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'status': '更新失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '更新失败', 'error': str(e)}, status=500)

def batch_delete_drugs(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        ids_to_delete = data.get('ids', [])

        if not ids_to_delete:
            return JsonResponse({'status': '删除失败', 'error': '未提供要删除的药品编号'}, status=400)

        delete_count, _ = Drug_information.objects.filter(编号__in=ids_to_delete).delete()

        return JsonResponse({'status': '删除成功', 'deleted_count': delete_count})
    except json.JSONDecodeError:
        return JsonResponse({'status': '删除失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '删除失败', 'error': str(e)}, status=500)


def user_list(request):
    users = User.objects.all().values()
    users_list = []
    for user in users:
        user_data = {
            '账号': user['账号'],
            '密码': user['密码'],
            '权限': user['权限'],
            '病人编号': user['病人编号'],
            '医生编号': user['医生编号']
        }
        users_list.append(user_data)
    return JsonResponse(users_list, safe=False)

def add_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        role = get_role_id(data['权限'])
        User.objects.create(
            账号=data['账号'],
            密码=data['密码'],
            权限=role,
            病人编号=data['病人编号'],
            医生编号=data['医生编号']
        )
        return JsonResponse({'message': 'User added successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def update_user(request, account):
    if request.method == 'PUT':
        data = json.loads(request.body)
        role = get_role_id(data['权限'])
        user = User.objects.get(账号=account)
        user.密码 = data['密码']
        user.权限 = role
        user.病人编号 = data['病人编号']
        user.医生编号 = data['医生编号']
        user.save()
        return JsonResponse({'message': 'User updated successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def delete_user(request, account):
    if request.method == 'DELETE':
        user = User.objects.get(账号=account)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_role_id(role_name):
    if role_name == '患者':
        return 0
    elif role_name == '管理员':
        return 1
    elif role_name == '医生':
        return 2
    else:
        return -1  # 返回错误值，以便处理未知角色的情况
    


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Fee_items
import json

@require_http_methods(["POST"])
def add_fee_item(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        item_id = data.get('编号')
        print(data)
        # 检查收费项目是否已存在
        if Fee_items.objects.filter(编号=item_id).exists():
            return JsonResponse({'status': '添加失败', 'error': '该编号已存在'}, status=400)

        # 添加新的收费项目
        new_item = Fee_items.objects.create(
            编号=item_id,
            名称=data.get('名称'),
            拼音码=data.get('拼音码'),
            费用=data.get('费用'),
            费用分类=data.get('费用分类'),
            病种分类=data.get('病种分类'),
            备注=data.get('备注')
        )
        print(new_item)
        return JsonResponse({'status': '添加成功', 'item_id': new_item.编号}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '添加失败', 'error': str(e)}, status=500)

@require_http_methods(["POST"])
def update_fee_item(request, item_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            item = Fee_items.objects.get(编号=item_id)
            item.编号 = data.get('编号', item.编号)
            item.名称 = data.get('名称', item.名称)
            item.拼音码 = data.get('拼音码', item.拼音码)
            item.费用 = data.get('费用', item.费用)
            item.费用分类 = data.get('费用分类', item.费用分类)
            item.病种分类 = data.get('病种分类', item.病种分类)
            item.备注 = data.get('备注', item.备注)
            item.save()
            print(item)
            return JsonResponse({'status': '更新成功', 'item_id': item.编号}, status=200)

        except Fee_items.DoesNotExist:
            return JsonResponse({'status': '更新失败', 'error': '收费项目不存在'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'status': '更新失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '更新失败', 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_fee_items(request):
    try:
        # 获取收费项目信息列表
        items = Fee_items.objects.all().values('编号', '名称', '拼音码', '费用', '费用分类', '病种分类', '备注')
        # 将QuerySet转换为列表，因为QuerySet不是JSON可序列化的
        items_list = list(items)
        return JsonResponse(items_list, safe=False)  # 设置safe=False以允许非字典对象
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def batch_delete_fee_items(request):
    try:
        # 解析请求体中的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))
        ids_to_delete = data.get('ids', [])  # 获取要删除的收费项目编号列表

        if not ids_to_delete:
            return JsonResponse({'status': '删除失败', 'error': '未提供要删除的收费项目编号'}, status=400)

        # 执行批量删除
        delete_count, _ = Fee_items.objects.filter(编号__in=ids_to_delete).delete()

        return JsonResponse({'status': '删除成功', 'deleted_count': delete_count})
    except json.JSONDecodeError:
        return JsonResponse({'status': '删除失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '删除失败', 'error': str(e)}, status=500)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Template
import json

@require_http_methods(["POST"])
def add_template(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        template_name = data.get('模板名称')

        if Template.objects.filter(模板名称=template_name).exists():
            return JsonResponse({'status': '添加失败', 'error': '该模板名称已存在'}, status=400)

        new_template = Template.objects.create(
            模板名称=template_name,
            主诉=data.get('主诉'),
            现病史=data.get('现病史'),
            往病史=data.get('往病史'),
            诊断=data.get('诊断'),
            检查=data.get('检查'),
            处方=data.get('处方')
        )

        return JsonResponse({'status': '添加成功', 'template_name': new_template.模板名称}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '添加失败', 'error': str(e)}, status=500)

@require_http_methods(["POST"])
def update_template(request, template_name):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            temp = Template.objects.get(模板名称=template_name)
            temp.主诉 = data.get('主诉', temp.主诉)
            temp.现病史 = data.get('现病史', temp.现病史)
            temp.往病史 = data.get('往病史', temp.往病史)
            temp.诊断 = data.get('诊断', temp.诊断)
            temp.检查 = data.get('检查', temp.检查)
            temp.处方 = data.get('处方', temp.处方)
            temp.save()

            return JsonResponse({'status': '更新成功', 'template_name': temp.模板名称}, status=200)

        except Template.DoesNotExist:
            return JsonResponse({'status': '更新失败', 'error': '模板不存在'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'status': '更新失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '更新失败', 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_templates(request):
    try:
        templates = Template.objects.all().values('模板名称', '主诉', '现病史', '往病史', '诊断', '检查', '处方')
        templates_list = list(templates)
        print(templates_list)
        return JsonResponse(templates_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def batch_delete_templates(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        names_to_delete = data.get('names', [])

        if not names_to_delete:
            return JsonResponse({'status': '删除失败', 'error': '未提供要删除的模板名称'}, status=400)

        delete_count, _ = Template.objects.filter(模板名称__in=names_to_delete).delete()

        return JsonResponse({'status': '删除成功', 'deleted_count': delete_count})
    except json.JSONDecodeError:
        return JsonResponse({'status': '删除失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '删除失败', 'error': str(e)}, status=500)
    
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Emr
import json

@require_POST
def add_emr(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        emr_id = data.get('病历编号')

        if not emr_id:
            return JsonResponse({'status': '添加失败', 'error': '未提供病历编号'}, status=400)

        if Emr.objects.filter(病历编号=emr_id).exists():
            return JsonResponse({'status': '添加失败', 'error': '该病历编号已存在'}, status=400)

        new_emr = Emr.objects.create(
            病历编号=emr_id,
            病人编号=data.get('病人编号'),
            姓名=data.get('姓名'),
            性别=data.get('性别'),
            年龄=data.get('年龄'),
            民族=data.get('民族'),
            费用类型=data.get('费用类型'),
            电话=data.get('电话'),
            医生姓名=data.get('医生姓名'),
            挂号科室=data.get('挂号科室'),
            主诉=data.get('主诉'),
            现病史=data.get('现病史'),
            往病史=data.get('往病史'),
            诊断=data.get('诊断'),
            检查=data.get('检查'),
            处方=data.get('处方')
        )

        return JsonResponse({'status': '添加成功', 'emr_id': new_emr.病历编号}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '添加失败', 'error': str(e)}, status=500)

@require_POST
def update_emr(request, emr_id):
    try:
        data = json.loads(request.body.decode('utf-8'))

        try:
            emr = Emr.objects.get(病历编号=emr_id)
            emr.姓名 = data.get('姓名', emr.姓名)
            emr.性别 = data.get('性别', emr.性别)
            emr.年龄 = data.get('年龄', emr.年龄)
            emr.民族 = data.get('民族', emr.民族)
            emr.费用类型 = data.get('费用类型', emr.费用类型)
            emr.电话 = data.get('电话', emr.电话)
            emr.医生姓名 = data.get('医生姓名', emr.医生姓名)
            emr.挂号科室 = data.get('挂号科室', emr.挂号科室)
            emr.主诉 = data.get('主诉', emr.主诉)
            emr.现病史 = data.get('现病史', emr.现病史)
            emr.往病史 = data.get('往病史', emr.往病史)
            emr.诊断 = data.get('诊断', emr.诊断)
            emr.检查 = data.get('检查', emr.检查)
            emr.处方 = data.get('处方', emr.处方)
            emr.save()

            return JsonResponse({'status': '更新成功', 'emr_id': emr.病历编号}, status=200)

        except Emr.DoesNotExist:
            return JsonResponse({'status': '更新失败', 'error': '病历编号不存在'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'status': '更新失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '更新失败', 'error': str(e)}, status=500)

def get_emr(request):
    try:
        emr_data = Emr.objects.all().values('病历编号', '姓名', '性别', '年龄', '民族', '费用类型', '电话')
        emr_list = list(emr_data)
        return JsonResponse(emr_list, safe=False, content_type='application/json')
    except Exception as e:
        return JsonResponse({'status': '获取失败', 'error': str(e)}, status=500)

@require_POST
def batch_delete_emr(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        ids_to_delete = data.get('ids', [])

        if not ids_to_delete:
            return JsonResponse({'status': '删除失败', 'error': '未提供要删除的病历编号'}, status=400)

        delete_count, _ = Emr.objects.filter(病历编号__in=ids_to_delete).delete()

        return JsonResponse({'status': '删除成功', 'deleted_count': delete_count})
    except json.JSONDecodeError:
        return JsonResponse({'status': '删除失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '删除失败', 'error': str(e)}, status=500)

def get_emr_details(request, emr_id):
    try:
        emr = Emr.objects.get(病历编号=emr_id)
        data = {
            '病历编号': emr.病历编号,
            '姓名': emr.姓名,
            '性别': emr.性别,
            '年龄': emr.年龄,
            '民族': emr.民族,
            '费用类型': emr.费用类型,
            '电话': emr.电话,
            '医生姓名': emr.医生姓名,
            '挂号科室': emr.挂号科室,
            '主诉': emr.主诉,
            '现病史': emr.现病史,
            '往病史': emr.往病史,
            '诊断': emr.诊断,
            '检查': emr.检查,
            '处方': emr.处方
        }
        return JsonResponse(data)
    except Emr.DoesNotExist:
        return JsonResponse({'error': '病历编号不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Drug_inventory
import json

def add_drug_inventory(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        drug_id = data.get('药品编号')

        # 添加新的药品库存信息
        new_drug_inventory = Drug_inventory(
            库房=data.get('库房'),
            药品编号=drug_id,
            药品数量=data.get('药品数量'),
            备注=data.get('备注')
        )
        new_drug_inventory.save()  # 保存时将自动生成库存编号

        return JsonResponse({'status': '添加成功', 'drug_inventory_id': new_drug_inventory.库存编号}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': '添加失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '添加失败', 'error': str(e)}, status=500)
    
@require_http_methods(["POST"])
def update_drug_inventory(request, inventory_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            drug_inventory = Drug_inventory.objects.get(库存编号=inventory_id)
            drug_inventory.库房 = data.get('库房', drug_inventory.库房)
            drug_inventory.药品编号 = data.get('药品编号', drug_inventory.药品编号)
            drug_inventory.药品数量 = data.get('药品数量', drug_inventory.药品数量)
            drug_inventory.备注 = data.get('备注', drug_inventory.备注)
            drug_inventory.save()

            return JsonResponse({'status': '更新成功', 'drug_inventory_id': drug_inventory.库存编号}, status=200)

        except Drug_inventory.DoesNotExist:
            return JsonResponse({'status': '更新失败', 'error': '药品库存不存在'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'status': '更新失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '更新失败', 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_drug_inventories(request):
    try:
        drug_inventories = Drug_inventory.objects.all().values('库存编号', '库房', '药品编号', '药品数量', '备注')
        drug_inventories_list = list(drug_inventories)
        return JsonResponse(drug_inventories_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def batch_delete_drug_inventories(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        ids_to_delete = data.get('ids', [])

        if not ids_to_delete:
            return JsonResponse({'status': '删除失败', 'error': '未提供要删除的药品库存编号'}, status=400)

        delete_count, _ = Drug_inventory.objects.filter(库存编号__in=ids_to_delete).delete()

        return JsonResponse({'status': '删除成功', 'deleted_count': delete_count})
    except json.JSONDecodeError:
        return JsonResponse({'status': '删除失败', 'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': '删除失败', 'error': str(e)}, status=500)

from .models import warehouse 
def get_warehouses(request):
    warehouses = warehouse.objects.values_list('名称',flat=True).distinct()
    return JsonResponse(list(warehouses), safe=False)

from .models import Outpatient_registration

@csrf_exempt
def outpatient_registrations(request):
    if request.method == 'GET':
        patient_id = request.GET.get('patientId', None)
        if patient_id:
            registrations = Outpatient_registration.objects.filter(病人编号=patient_id)
        else:
            registrations = Outpatient_registration.objects.all()
        
        data = []
        for registration in registrations:
            data.append({
                '编号': registration.编号,
                '挂号科室': registration.挂号科室,
                '费用类型': registration.费用类型,
                '挂号类型': registration.挂号类型,
                '挂号费用': float(registration.挂号费用),
                '医生': registration.医生,
                '时间': registration.时间.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'})
    

def get_emrs(request):
    patient_id = request.GET.get('patientId')
    if patient_id:
        emrs = Emr.objects.filter(病人编号=patient_id)
        emr_data = []
        for emr in emrs:
            emr_data.append({
                '病历编号': emr.病历编号,
                '挂号科室': emr.挂号科室,
                '费用类型': emr.费用类型,
                '医生姓名': emr.医生姓名,
                '主诉':emr.主诉,
                '现病史':emr.现病史,
                '往病史' :emr.往病史,
                '诊断':emr.诊断,
                '检查':emr.检查,
                '处方':emr.处方,
            })
        return JsonResponse(emr_data, safe=False)
    else:
        return JsonResponse({'error': 'Patient ID not provided'}, status=400)
    

import json
from .models import Outpatient_registration, Registration_type

@csrf_exempt
def get_outpatient_registrations(request):
    if request.method == 'GET':
        registrations = list(Outpatient_registration.objects.values())
        return JsonResponse(registrations, safe=False)

@csrf_exempt
def add_outpatient_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        registration = Outpatient_registration.objects.create(
            编号=data['编号'],
            病人编号=data['病人编号'],
            姓名=data['姓名'],
            性别=data['性别'],
            挂号科室=data['挂号科室'],
            费用类型=data['费用类型'],
            挂号类型=data['挂号类型'],
            挂号费用=data['挂号费用'],
            医生=data['医生'],
            时间=data['时间'],
        )
        return JsonResponse({"message": "门诊挂号信息添加成功"})

@csrf_exempt
def update_outpatient_registration(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        registration = Outpatient_registration.objects.filter(编号=id).update(
            病人编号=data['病人编号'],
            姓名=data['姓名'],
            性别=data['性别'],
            挂号科室=data['挂号科室'],
            费用类型=data['费用类型'],
            挂号类型=data['挂号类型'],
            挂号费用=data['挂号费用'],
            医生=data['医生'],
            时间=data['时间'],
        )
        return JsonResponse({"message": "门诊挂号信息更新成功"})

@csrf_exempt
def delete_outpatient_registration(request, id):
    if request.method == 'DELETE':
        registration = Outpatient_registration.objects.get(编号=id)
        registration.delete()
        return JsonResponse({"message": "门诊挂号信息删除成功"})


@csrf_exempt
def get_doctors(request):
    if request.method == 'GET':
        department_name = request.GET.get('department', None)
        if department_name:
            doctors = doctor.objects.filter(科室=department_name).values_list('姓名', flat=True)
            #print(doctors)
            return JsonResponse(list(doctors), safe=False)
        else:
            return JsonResponse({"message": "请提供科室信息"}, status=400)
        
def get_doctor_remark(request):
    doctor_name = request.GET.get('doctor', '')
    if not doctor_name:
        return JsonResponse({'error': 'Doctor name is required'}, status=400)
    try:
        doctor_obj = doctor.objects.get(姓名=doctor_name)
        doctor_remark = doctor_obj.备注
        return JsonResponse({'remark': doctor_remark})
    except doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_registration_type(request):
    remark = request.GET.get('remark', '')
    registration_type_objs = Registration_type.objects.filter(挂号类型=remark)
    if registration_type_objs.exists():
        registration_type = registration_type_objs.first()
        return JsonResponse({'type': registration_type.挂号类型})
    else:
        return JsonResponse({'error': 'Registration type not found'}, status=404)

def get_registration_fee(request):
    registration_type = request.GET.get('type', '')
    registration_fee_objs = Registration_type.objects.filter(挂号类型=registration_type)
    if registration_fee_objs.exists():
        registration_fee = registration_fee_objs.first()
        return JsonResponse({'fee': registration_fee.挂号费})
    else:
        return JsonResponse({'error': 'Registration fee not found'}, status=404)

from django.db.models import Count

def get_registration_data(request):
    try:
        # 获取挂号人数随时间变化的数据
        count_data = Outpatient_registration.objects.values('时间').annotate(count=Count('时间')).order_by('时间')
        
        # 获取挂号科室占比的数据
        department_data = Outpatient_registration.objects.values('挂号科室').annotate(count=Count('挂号科室'))
        
        # 格式化数据
        count_data = [{'value': item['count'], 'name': str(item['时间'])} for item in count_data]
        department_data = [{'value': item['count'], 'name': item['挂号科室']} for item in department_data]
        print(department_data)
        print(count_data)
        return JsonResponse({
            'countData': count_data,
            'departmentData': department_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
from .models import Drug_inventory, Drug_information

def get_drug_inventory(request):
    # 获取药品库存数据
    drug_inventory_data = list(Drug_inventory.objects.all().values())
    return JsonResponse(drug_inventory_data, safe=False)

def get_drug_information(request):
    # 获取药品资料数据
    drug_information_data = list(Drug_information.objects.all().values())
    return JsonResponse(drug_information_data, safe=False)

from .models import Outpatient_registration, Outpatient_pricing
import logging

# 获取logger实例
logger = logging.getLogger(__name__)

@require_POST
def save_outpatient_registration(request):
    try:
        data = json.loads(request.body)
        print(data)
        outpatient_number = data.get('outpatientNumber') # 获取门诊挂号编号
        logger.debug(f"Received outpatient number: {outpatient_number}")  # 添加日志记录
        registration = Outpatient_registration.objects.create(
            编号=outpatient_number,
            病人编号=data.get('patientId'),
            姓名=data.get('patientName'),
            性别=data.get('patientGender'),
            挂号科室=data.get('department'),
            医生=data.get('doctor'),
            时间=data.get('appointmentDate'),
            挂号费用=data.get('registrationFees'),
            挂号类型=data.get('registrationType'),
            费用类型=data.get('patientInfoType'),
            是否已划价='否'
        )
        logger.info(f"Outpatient registration created successfully: {registration}")
        return JsonResponse({'success': True, 'outpatientNumber': outpatient_number})
    except Exception as e:
        error_message = f"Error saving outpatient registration: {str(e)}"
        logger.error(error_message)
        return JsonResponse({'success': False, 'error': error_message})

import datetime
import random
    
@require_POST
def save_outpatient_pricing(request):
    now = datetime.datetime.now()
    random_number = random.randint(100, 999)  # 生成一个 4 位的随机数
    outpatient_numbers = f"{now.strftime('%Y%m%d')}{random_number}"
    data = json.loads(request.body)
    logger.info(f"Received data in save_outpatient_pricing: {data}")  # 添加日志记录
    try:
        outpatient_number = data.get('outpatientNumber')  # 获取门诊挂号编号
        if not outpatient_number:
            raise ValueError("Outpatient number is missing")

        pricing = Outpatient_pricing.objects.create(
            编号= outpatient_numbers,
            挂号编号=outpatient_number,
            科室=data.get('department'),
            医生=data.get('doctor'),
            是否收费='否'
        )
        logger.info(f"Outpatient pricing created successfully: {pricing}")
        return JsonResponse({'success': True})
    except Exception as e:
        error_message = f"Error saving outpatient pricing: {str(e)}"
        logger.error(error_message)
        return JsonResponse({'success': False, 'error': error_message})

from django.http import JsonResponse
from .models import User, doctor, Outpatient_registration
def get_doctor_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        # 根据用户名获取用户信息
        try:
            user = User.objects.get(账号=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
        doctor_id = user.医生编号 
        return JsonResponse({'doctorId': doctor_id})

def get_doctor_name(request, doctor_id):
    # 根据医生编号获取医生姓名
    try:
        doctor_obj = doctor.objects.get(编号=doctor_id)
    except doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor does not exist'}, status=400)

    doctor_name = doctor_obj.姓名
   
    return JsonResponse({'doctorName': doctor_name})

def get_outpatient_records(request, doctor_name):
    # 根据医生姓名获取门诊挂号记录
    try:
        records = Outpatient_registration.objects.filter(医生=doctor_name)
        outpatient_records = [{
            '编号': record.编号,
            '姓名': record.姓名,
            '病人编号':record.病人编号,
            '挂号科室': record.挂号科室,
            '费用类型': record.费用类型,
            '挂号类型': record.挂号类型,
            '挂号费用': str(record.挂号费用),  # 将费用转换为字符串
            '时间': record.时间,
            '是否已划价': record.是否已划价,
        } for record in records]
    except Outpatient_registration.DoesNotExist:
        return JsonResponse({'error': 'Outpatient records not found'}, status=400)

    return JsonResponse({'outpatientRecords': outpatient_records})

def get_patient_info(request, patient_id):
    # 根据病人编号获取病人信息
    try:
        new_patient = patient.objects.get(编号=patient_id)
        patient_info = {
            '病人编号':patient_id,
            '姓名': new_patient.姓名,
            '性别': new_patient.性别,
            '年龄': new_patient.年龄,
            '民族': new_patient.民族,
            '电话': new_patient.电话,
            '费用类型':new_patient.费用类型,
        }
        return JsonResponse(patient_info)
    except patient.DoesNotExist:
        return JsonResponse({'error': 'Patient does not exist'}, status=400)

def get_doctor_info(request, doctor_id):
    # 根据医生编号获取医生信息
    try:
        doctor_obj = doctor.objects.get(编号=doctor_id)
        # 假设 doctor 模型有以下字段：姓名、性别、科室、出生日期、入职日期
        doctor_info = {
            '医生姓名': doctor_obj.姓名,
            '挂号科室': doctor_obj.科室,
        }
        return JsonResponse(doctor_info)
    except doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor does not exist'}, status=400)

@csrf_exempt
def get_drug_names(request):
    # 从药品资料表中获取药品名称列表
    drug_names = list(Drug_information.objects.values_list('名称', flat=True))
    return JsonResponse(drug_names, safe=False)

@csrf_exempt
def get_fee_item_names(request):
    # 从门诊收费项目表中获取收费项目名称列表
    fee_item_names = list(Fee_items.objects.values_list('名称', flat=True))
    return JsonResponse(fee_item_names, safe=False)

@csrf_exempt
def save_emr(request):
    if request.method == 'POST':
        emr_data = json.loads(request.body)
        prescriptions = emr_data.get('处方', [])
        examinations = emr_data.get('检查', [])

        emr = Emr.objects.create(
            病历编号=generate_emr_number(),  # 自动生成病历编号
            病人编号=emr_data.get('病人编号', ''),
            姓名=emr_data.get('姓名', ''),
            性别=emr_data.get('性别', ''),
            年龄=emr_data.get('年龄', ''),
            民族=emr_data.get('民族', ''),
            费用类型=emr_data.get('费用类型', ''),
            电话=emr_data.get('电话', ''),
            医生姓名=emr_data.get('医生姓名', ''),
            挂号科室=emr_data.get('挂号科室', ''),
            主诉=emr_data.get('主诉', ''),
            现病史=emr_data.get('现病史', ''),
            往病史=emr_data.get('往病史', ''),
            诊断=emr_data.get('诊断', ''),
        )

        for prescription in prescriptions:
            drug_name = prescription.get('name', '')
            quantity = prescription.get('quantity', '')
            # 在药品资料库中查找药品信息
            drug = Drug_information.objects.filter(名称=drug_name).first()
            if drug:
                outpatient_detail = Outpatient_details.objects.create(
                    划价编号=emr.病历编号,
                    药品编号=drug.编号,
                    单价=drug.出库单价,
                    数量=quantity,
                    金额=float(drug.出库单价) * float(quantity)
                )

        for examination in examinations:
            examination_name = examination.get('name', '')
            quantity = examination.get('quantity', '')
            # 在门诊收费项目中查找收费项目信息
            fee_item = Fee_items.objects.filter(名称=examination_name).first()
            if fee_item:
                outpatient_detail = Outpatient_details.objects.create(
                    划价编号=emr.病历编号,
                    药品编号=fee_item.编号,
                    单价=fee_item.费用,
                    数量=quantity,
                    金额=float(fee_item.费用) * float(quantity)
                )

        return JsonResponse({'message': '病历保存成功'})
    else:
        return JsonResponse({'message': '仅支持 POST 请求'})

from django.utils import timezone

def generate_emr_number():
    # 使用当前时间戳生成病历编号
    timestamp = timezone.now().strftime('%Y%m%d%H')  # 格式为年月日时分秒微秒
    return 'EMR_' + timestamp


from .models import Outpatient_details

def get_outpatient_details(request):
    if request.method == 'GET':
        outpatient_details = list(Outpatient_details.objects.all().values())
        return JsonResponse(outpatient_details, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported method'}, status=405)

@csrf_exempt
def get_emr_number(request):
    if request.method == 'POST':
        patient_id = json.loads(request.body).get('patientId', '')
        if patient_id:
            try:
                # 根据病人编号查询病历编号
                emrs = Emr.objects.filter(病人编号=patient_id)
                if emrs.exists():
                    # 返回所有匹配的病历编号
                    emr_numbers = [emr.病历编号 for emr in emrs]
                    print(emr_numbers)
                    return JsonResponse({'emrNumbers': emr_numbers})
                else:
                    return JsonResponse({'error': 'No EMR found for the patient ID'}, status=404)
            except Emr.DoesNotExist:
                return JsonResponse({'error': 'No EMR found for the patient ID'}, status=404)
        else:
            return JsonResponse({'error': 'Patient ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


@csrf_exempt
def get_outpatient_details(request, emr_number):
    if request.method == 'GET':
        try:
            # 根据单个病历编号查询对应的门诊划价明细数据
            outpatient_details = Outpatient_details.objects.filter(划价编号=emr_number).values()
            return JsonResponse({'emrNumber': emr_number, 'outpatientDetails': list(outpatient_details)})
        except Outpatient_details.DoesNotExist:
            return JsonResponse({'error': 'No outpatient details found for the EMR number'}, status=404)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)



