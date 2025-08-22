# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class area(models.Model):
    编号 = models.CharField(primary_key=True, max_length=20)
    产地名称 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '产地'


class doctor(models.Model):
    编号 = models.CharField(primary_key=True, max_length=15)
    姓名 = models.CharField(max_length=20)
    性别 = models.CharField(max_length=2, blank=True, null=True)
    科室 = models.CharField(max_length=20, blank=True, null=True)
    备注 = models.CharField(max_length=50, blank=True, null=True)
    出生日期 = models.DateTimeField(blank=True, null=True)
    入职日期 = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed =False
        db_table = '医生资料'


class warehouse(models.Model):
    编号 = models.CharField(primary_key=True, max_length=5)
    名称 = models.CharField(max_length=50, blank=True, null=True)
    位置 = models.CharField(max_length=100, blank=True, null=True)
    备注 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '库房资料'


class User(models.Model):
    账号 = models.CharField(primary_key=True,max_length=255)
    密码 = models.CharField(max_length=255)
    权限 = models.CharField(max_length=255)
    病人编号 = models.CharField(max_length=255, null=True, blank=True) 
    医生编号 = models.CharField(max_length=255, null=True, blank=True) 
    class Meta:
        managed = True
        db_table = '用户管理'


class patient(models.Model):
    编号 = models.CharField(primary_key=True, max_length=15)
    姓名 = models.CharField(max_length=30, blank=True, null=True)
    性别 = models.CharField(max_length=4, blank=True, null=True)
    年龄 = models.IntegerField(blank=True, null=True)
    民族 = models.CharField(max_length=20, blank=True, null=True)
    费用类型 = models.CharField(max_length=20, blank=True, null=True)
    电话 = models.CharField(max_length=15, blank=True, null=True)
    拼音码 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '病人信息库'


class department(models.Model):
    编号 = models.CharField(primary_key=True, max_length=10)
    名称 = models.CharField(max_length=20, blank=True, null=True)
    备注 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '科室资料'


class position(models.Model):
    编号 = models.CharField(primary_key=True, max_length=20)
    名称 = models.CharField(max_length=20, blank=True, null=True)
    备注 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '职务资料'


class Drug_classification(models.Model):
    编号 = models.CharField(primary_key=True, max_length=20)
    名称 = models.CharField(max_length=50, blank=True, null=True)
    备注 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '药品分类'


class Drug_inventory(models.Model):
    库存编号 = models.AutoField(primary_key=True)
    库房 = models.CharField(max_length=50, blank=True, null=True)
    药品编号 = models.CharField(max_length=20)
    药品数量 = models.DecimalField(max_digits=12, decimal_places=2)
    备注 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '药品库存'


class Drug_information(models.Model):
    编号 = models.CharField(primary_key=True, max_length=20)
    名称 = models.CharField(max_length=50)
    规格 = models.CharField(max_length=50, blank=True, null=True)
    整量单位 = models.CharField(max_length=50, blank=True, null=True)
    散量单位 = models.CharField(max_length=50, blank=True, null=True)
    入库单价 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    出库单价 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    批发价 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    整散比 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    分类 = models.CharField(max_length=50, blank=True, null=True)
    费用归类 = models.CharField(max_length=50, blank=True, null=True)
    拼音码 = models.CharField(max_length=50, blank=True, null=True)
    效期 = models.CharField(max_length=20, blank=True, null=True)
    上限 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    下限 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '药品资料'


class unit(models.Model):
    编号 = models.CharField(primary_key=True, max_length=5)
    名称 = models.CharField(max_length=20, blank=True, null=True)
    备注 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '计量单位'


class Outpatient_pricing(models.Model):
    编号 = models.CharField(primary_key=True, max_length=15)
    科室 = models.CharField(max_length=30, blank=True, null=True)
    挂号编号 = models.CharField(max_length=15, blank=True, null=True)
    医生 = models.CharField(max_length=10, blank=True, null=True)
    划价时间 = models.DateTimeField(blank=True, null=True)
    划价员 = models.CharField(max_length=10, blank=True, null=True)
    是否收费 = models.CharField(max_length=2, blank=True, null=True)
    收费员 = models.CharField(max_length=10, blank=True, null=True)
    收费时间 = models.DateTimeField(blank=True, null=True)
    划价金额 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    是否发药 = models.CharField(max_length=2, blank=True, null=True)
    发药时间 = models.DateTimeField(blank=True, null=True)
    发药员 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '门诊划价'


class Outpatient_details(models.Model):
    编号 = models.SmallAutoField(primary_key=True)
    划价编号 = models.CharField(max_length=15)
    药品编号 = models.CharField(max_length=20)
    单价 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    数量 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    金额 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '门诊划价明细'


class Outpatient_registration(models.Model):
    编号 = models.CharField(primary_key=True, max_length=15)
    病人编号 = models.CharField(max_length=15, blank=True, null=True)
    姓名 = models.CharField(max_length=30, blank=True, null=True)
    性别 = models.CharField(max_length=2, blank=True, null=True)
    挂号科室 = models.CharField(max_length=30, blank=True, null=True)
    费用类型 = models.CharField(max_length=30, blank=True, null=True)
    挂号类型 = models.CharField(max_length=30, blank=True, null=True)
    挂号费用 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    医生 = models.CharField(max_length=30, blank=True, null=True)
    时间 = models.DateTimeField(blank=True, null=True)
    是否已划价 = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '门诊挂号'


class Registration_type(models.Model):
    编号 = models.IntegerField(primary_key=True)
    挂号类型 = models.CharField(max_length=20, blank=True, null=True)
    挂号费 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '门诊挂号类型'


class Fee_items(models.Model):
    编号 = models.CharField(primary_key=True, max_length=20)
    名称 = models.CharField(max_length=100)
    拼音码 = models.CharField(max_length=20, blank=True, null=True)
    费用 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    费用分类 = models.CharField(max_length=50, blank=True, null=True)
    病种分类 = models.CharField(max_length=50, blank=True, null=True)
    备注 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '门诊收费项目'

class Emr(models.Model):
    病历编号 = models.CharField(primary_key=True, max_length=255)
    病人编号 = models.CharField( max_length=15)
    姓名 = models.CharField(max_length=30, blank=True, null=True)
    性别 = models.CharField(max_length=2, blank=True, null=True)
    年龄 = models.IntegerField(blank=True, null=True)
    民族 = models.CharField(max_length=20, blank=True, null=True)
    费用类型 = models.CharField(max_length=20, blank=True, null=True)
    电话 = models.CharField(max_length=15, blank=True, null=True)
    医生姓名 = models.CharField(max_length=30, blank=True, null=True)
    挂号科室 = models.CharField(max_length=30, blank=True, null=True)
    主诉 = models.CharField(max_length=255,blank=True, null=True)
    现病史 = models.CharField(max_length=255, blank=True, null=True)
    往病史 = models.CharField(max_length=255, blank=True, null=True)
    诊断 = models.CharField(max_length=255, blank=True, null=True)
    检查= models.CharField(max_length=255, blank=True, null=True)
    处方= models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = '电子病历'

        
class Template(models.Model):
    模板名称=models.CharField(primary_key=True, max_length=255)
    主诉 = models.CharField(max_length=255,blank=True, null=True)
    现病史 = models.CharField(max_length=255, blank=True, null=True)
    往病史 = models.CharField(max_length=255, blank=True, null=True)
    诊断 = models.CharField(max_length=255, blank=True, null=True)
    检查= models.CharField(max_length=255, blank=True, null=True)
    处方= models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = '病历模板'