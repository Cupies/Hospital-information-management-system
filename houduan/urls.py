"""houduan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from myapp import views
from  django.views.generic.base import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name="index.html")),
    path('register/', views.register,name='register'),
    path('login/', views.login_view, name='login'),
    path('bind_number/', views.bind_number_view, name='bind_number'),
    
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('departments/', views.get_departments, name='get_departments'),
    path('doctor/update/<str:doctor_id>/', views.update_doctor, name='update_doctor'),
    path('doctor/delete/', views.batch_delete, name='batch_delete'),
    path('doctor/add/', views.add_doctor, name='add_doctor'),
    path('get_registrationTypes/', views.get_registrationTypes, name='get_registrationTypes'),

    path('patients/', views.get_patients, name='get_patients'),
    path('patient/add/', views.add_patient, name='add_patient'),
    path('patients/delete/', views.batch_delete_patients, name='batch_delete_patients'),
    path('patient/update/<str:patient_id>/', views.update_patient, name='update_patient'),
    path('patient/<str:patient_id>/', views.get_patient_info, name='get_patient_info'),
    path('patient/update-info/<str:patient_id>/', views.update_patient_info, name='update_patient_info'),
    path('get-patient-id/', views.get_patient_id, name='get_patient_id'),


    path('drugs/', views.get_drugs, name='get_drugs'),
    path('drugs/add/', views.add_drug, name='add_drug'),
    path('drugs/update/<str:drug_id>/', views.update_drug, name='update_drug'),
    path('drugs/batch_delete/', views.batch_delete_drugs, name='batch_delete_drugs'),

    path('users/', views.user_list, name='user-list'),
    path('users/add/', views.add_user, name='add-user'),
    path('users/<str:account>/', views.update_user, name='update-user'),
    path('users/<str:account>/delete/', views.delete_user, name='delete-user'),

    path('fee_items/', views.get_fee_items, name='get_fee_items'),
    path('fee_items/add/', views.add_fee_item, name='add_fee_item'),
    path('fee_items/update/<str:item_id>/', views.update_fee_item, name='update_fee_item'),
    path('fee_items/delete/', views.batch_delete_fee_items, name='batch_delete_fee_items'),

    path('add_template/', views.add_template, name='add_template'),
    path('update_template/<str:template_name>/', views.update_template, name='update_template'),
    path('get_templates/', views.get_templates, name='get_templates'),
    path('batch_delete_templates/', views.batch_delete_templates, name='batch_delete_templates'),

    path('add_emr/', views.add_emr, name='add_emr'),
    path('update_emr/<str:emr_id>/', views.update_emr, name='update_emr'),
    path('get_emr/', views.get_emr, name='get_emr'),
    path('batch_delete_emr/', views.batch_delete_emr, name='batch_delete_emr'),
    path('get_emr_details/<str:emr_id>/', views.get_emr_details, name='get_emr_details'),
    path('emrs/', views.get_emrs, name='emrs'),

    path('add_drug_inventory/', views.add_drug_inventory, name='add_drug_inventory'),
    path('update_drug_inventory/<int:inventory_id>/', views.update_drug_inventory, name='update_drug_inventory'),
    path('get_drug_inventories/', views.get_drug_inventories, name='get_drug_inventories'),
    path('batch_delete_drug_inventories/', views.batch_delete_drug_inventories, name='batch_delete_drug_inventories'),
    path('warehouses/', views.get_warehouses, name='get_warehouses'),

    path('outpatient_registrations/', views.outpatient_registrations, name='outpatient_registrations'),
    path('get_outpatient_registrations/', views.get_outpatient_registrations, name='get_outpatient_registrations'),
    path('add_outpatient_registration/', views.add_outpatient_registration, name='add_outpatient_registration'),
    path('update_outpatient_registration/<int:id>/', views.update_outpatient_registration, name='update_outpatient_registration'),
    path('delete_outpatient_registration/<int:id>/', views.delete_outpatient_registration, name='delete_outpatient_registration'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),

    path('doctor_remarks/', views.get_doctor_remark, name='doctor_remarks'),
    path('registration_types/', views.get_registration_type, name='registration_types'),
    path('registration_fees/', views.get_registration_fee, name='registration_fees'),

    path('get-registration-data/', views.get_registration_data, name='get-registration_data'),
     path('get-drug-inventory/', views.get_drug_inventory, name='get_drug_inventory'),
    path('get-drug-information/', views.get_drug_information, name='get_drug_information'),

    path('save_outpatient_registration/', views.save_outpatient_registration, name='save_outpatient_registration'),
    path('save_outpatient_pricing/', views.save_outpatient_pricing, name='save_outpatient_pricing'),

    path('get-doctor-id/', views.get_doctor_id, name='get_doctor_id'),
    path('get-doctor-name/<str:doctor_id>/', views.get_doctor_name, name='get_doctor_name'),
    path('get-outpatient-records/<str:doctor_name>/', views.get_outpatient_records, name='get_outpatient_records'),

    path('get-patient-info/<str:patient_id>/', views.get_patient_info, name='get_patient_info'),
    path('get-doctor-info/<str:doctor_id>/', views.get_doctor_info, name='get_doctor_info'),
    path('get-drug-names/', views.get_drug_names, name='get_drug_names'),
    path('get-fee-item-names/', views.get_fee_item_names, name='get_fee_item_names'),
    path('save_emr/', views.save_emr, name='save_emr'),

    path('outpatient_details/', views.outpatient_details, name='outpatient_details'),
     path('get-emr-number/', views.get_emr_number, name='get_emr_number'),
    path('get-outpatient-details/<str:emr_number>/', views.get_outpatient_details, name='get_outpatient_details'),
]
