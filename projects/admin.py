from django.contrib import admin
from .models import Project, Beneficiary, Activity, Report


# =========================
# 📋 PROJECT
# =========================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'status', 'progress', 'created_at']
    search_fields = ['name', 'description', 'region']
    list_filter = ['status', 'category', 'region']
    ordering = ['-created_at']


# =========================
# 👥 BENEFICIARY
# =========================
@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'age', 'project', 'created_at']
    search_fields = ['first_name', 'last_name', 'region']
    list_filter = ['gender', 'region', 'project']
    ordering = ['-created_at']


# =========================
# 📊 ACTIVITY
# =========================
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['type', 'project', 'agent', 'date', 'status']
    search_fields = ['description', 'result']
    list_filter = ['status', 'type', 'project']
    ordering = ['-date']


# =========================
# 📄 REPORT
# =========================
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'start_date', 'end_date', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['project']
    ordering = ['-created_at']