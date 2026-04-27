from django.urls import path
from .views import (
    activity_detail,
    agent_dashboard,
    assign_agent,
    beneficiary_list,
    create_activity,
    activity_list,
    create_beneficiary,
    create_report,
    delete_beneficiary,
    export_report_pdf,
    project_detail,
    report_detail,
    report_list,
    update_beneficiary,
    project_list,
    create_project,
    update_project,
    delete_project,
    close_project,
    validate_activity,
    reject_activity,
    update_activity,
    beneficiary_detail,
    delete_activity
)

urlpatterns = [

    # =========================
    # 📋 PROJETS
    # =========================
    path('', project_list, name='project_list'),
    path('create/', create_project, name='create_project'),
    path('update/<int:id>/', update_project, name='update_project'),
    path('delete/<int:id>/', delete_project, name='delete_project'),
    path('close/<int:id>/', close_project, name='close_project'),
    path('detail/<int:id>/', project_detail, name='project_detail'),
    path('assign-agent/<int:id>/', assign_agent, name='assign_agent'),

    # =========================
    # 👷 AGENT
    # =========================
    path('agent/dashboard/', agent_dashboard, name='agent_dashboard'),

    # =========================
    # 👥 BÉNÉFICIAIRES
    # =========================
    path('beneficiaires/', beneficiary_list, name='beneficiary_list'),
    path('beneficiaires/create/', create_beneficiary, name='create_beneficiary'),
    path('beneficiaires/update/<int:id>/', update_beneficiary, name='update_beneficiary'),
    path('beneficiaires/<int:id>/', beneficiary_detail, name='beneficiary_detail'),
    path('beneficiaires/delete/<int:id>/', delete_beneficiary, name='delete_beneficiary'),

    # =========================
    # 📊 ACTIVITÉS
    # =========================
    path('activities/', activity_list, name='activity_list'),
    path('activities/create/', create_activity, name='create_activity'),
    path('activities/update/<int:id>/', update_activity, name='update_activity'),
    path('activities/delete/<int:id>/', delete_activity, name='delete_activity'),
    path('activities/validate/<int:id>/', validate_activity, name='validate_activity'),
    path('activities/reject/<int:id>/', reject_activity, name='reject_activity'),
    path('activities/<int:id>/', activity_detail, name='activity_detail'),

    # =========================
    # 📄 RAPPORTS
    # =========================
    path('rapports/', report_list, name='report_list'),
    path('rapports/nouveau/', create_report, name='create_report'),
    path('rapports/<int:id>/', report_detail, name='report_detail'),
    path('rapports/<int:id>/pdf/', export_report_pdf, name='export_report_pdf'),
]