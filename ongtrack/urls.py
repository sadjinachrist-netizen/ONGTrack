"""
URL configuration for ongtrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from projects.models import Project, Beneficiary
from projects.views import redirect_dashboard


def dashboard(request):
    projects = Project.objects.all()
    beneficiaries = Beneficiary.objects.all()

    total_men = beneficiaries.filter(gender='homme').count()
    total_women = beneficiaries.filter(gender='femme').count()

    project_data = []
    for project in projects:
        count = project.beneficiaries.count()
        project_data.append({
            'name': project.name,
            'count': count
        })

    context = {
        'projects': projects,
        'total_projects': projects.count(),
        'total_beneficiaries': beneficiaries.count(),
        'total_men': total_men,
        'total_women': total_women,
        'project_data': project_data,
    }

    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # 🔥 Dashboard responsable
    path('responsable/dashboard/', dashboard, name='responsable_dashboard'),

    # 🔥 ROUTE PRINCIPALE (TRÈS IMPORTANT)
    path('dashboard/', redirect_dashboard, name='redirect_dashboard'),

    # 🔥 APP PROJECTS
    path('projects/', include('projects.urls')),
]