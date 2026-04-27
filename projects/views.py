from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Q
from xhtml2pdf import pisa
from django.contrib import messages
from .models import Project, Beneficiary, Activity, Report
from .forms import (
    ProjectForm,
    BeneficiaryForm,
    ActivityForm,
    ReportForm,
    AssignAgentForm
)

# =========================
# 📋 PROJETS
# =========================

@login_required
def project_list(request):

    user = request.user

    if user.is_staff:
        # 🔥 RESPONSABLE → projets où il est assigné
        projects = Project.objects.filter(assigned_agents=user)

        reports = Report.objects.filter(project__in=projects)

    else:
        # 🔥 AGENT → ses rapports seulement
        reports = Report.objects.filter(activity__agent=user)

    return render(request, 'reports/report_list.html', {
        'reports': reports
    })



def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form})


def update_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {'form': form})


def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect('project_list')


def close_project(request, id):
    project = get_object_or_404(Project, id=id)
    project.status = "termine"
    project.progress = 100
    project.save()
    return redirect('project_list')


@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)

    beneficiaries = project.beneficiaries.all()
    activities = project.activities.all().order_by('-date')
    agents = project.assigned_agents.all()

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'beneficiaries': beneficiaries,
        'activities': activities,
        'agents': agents
    })


# =========================
# 👥 AFFECTATION AGENT
# =========================

@login_required
def assign_agent(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        form = AssignAgentForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = AssignAgentForm(instance=project)

    return render(request, 'projects/assign_agent.html', {
        'form': form,
        'project': project
    })


# =========================
# 👷 DASHBOARD AGENT
# =========================

@login_required
def agent_dashboard(request):
    user = request.user

    projects = Project.objects.filter(assigned_agents=user)
    beneficiaries = Beneficiary.objects.filter(project__in=projects)

    # 🔥 Activités récentes
    activities = Activity.objects.filter(agent=user).order_by('-date')[:5]


    return render(request, 'agent/dashboard_agent.html', {
        'projects': projects,
        'total_projects': projects.count(),
        'total_beneficiaries': beneficiaries.count(),
        'activities_this_month': Activity.objects.filter(agent=user).count(),
        'recent_activities': activities,

        
    })


# =========================
# 🔁 REDIRECTION
# =========================

@login_required
def redirect_dashboard(request):
    if request.user.is_superuser:
        return redirect('/responsable/dashboard/')
    else:
        return redirect('/projects/agent/dashboard/')


# =========================
# 👥 BÉNÉFICIAIRES
# =========================


@login_required
def beneficiary_list(request):

    if request.user.is_superuser:
        beneficiaries = Beneficiary.objects.all()
    else:
        projects_user = Project.objects.filter(assigned_agents=request.user)
        beneficiaries = Beneficiary.objects.filter(project__in=projects_user)

    # 🔍 RECHERCHE TEXTE (propre)
    query = request.GET.get('q')
    if query:
        beneficiaries = beneficiaries.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(region__icontains=query)
        )

    # 🎯 FILTRE PROJET
    project_id = request.GET.get('project')
    if project_id:
        beneficiaries = beneficiaries.filter(project_id=project_id)

    # 🎯 FILTRE SEXE
    gender = request.GET.get('gender')
    if gender:
        beneficiaries = beneficiaries.filter(gender=gender)

    # 🎯 FILTRE RÉGION
    region = request.GET.get('region')
    if region:
        beneficiaries = beneficiaries.filter(region__icontains=region)

    projects = Project.objects.all()

    return render(request, 'beneficiaries/beneficiary_list.html', {
        'beneficiaries': beneficiaries,
        'projects': projects
    })


@login_required
def create_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_list')
    else:
        form = BeneficiaryForm(user=request.user)

    return render(request, 'beneficiaries/beneficiary_form.html', {'form': form})


@login_required
def update_beneficiary(request, id):
    beneficiary = get_object_or_404(Beneficiary, id=id)

    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_list')
    else:
        form = BeneficiaryForm(instance=beneficiary, user=request.user)

    return render(request, 'beneficiaries/beneficiary_form.html', {'form': form})


@login_required
def beneficiary_detail(request, id):
    beneficiary = get_object_or_404(Beneficiary, id=id)

    if not request.user.is_superuser:
        if beneficiary.project not in Project.objects.filter(assigned_agents=request.user):
            return redirect('beneficiary_list')

    return render(request, 'beneficiaries/beneficiary_detail.html', {
        'beneficiary': beneficiary
    })


@login_required
def delete_beneficiary(request, id):
    beneficiary = get_object_or_404(Beneficiary, id=id)

    # 🔐 SEUL RESPONSABLE SUPPRIME
    if not request.user.is_superuser:
        return redirect('beneficiary_list')

    beneficiary.delete()
    return redirect('beneficiary_list')


# =========================
# 📊 ACTIVITÉS
# =========================


@login_required
def activity_list(request):

    if request.user.is_superuser:
        activities = Activity.objects.all()
    else:
        projects = Project.objects.filter(assigned_agents=request.user)
        activities = Activity.objects.filter(project__in=projects)

    # 🔍 recherche
    q = request.GET.get('q')
    if q:
        activities = activities.filter(
            Q(description__icontains=q) |
            Q(result__icontains=q)
        )

    # 🎯 filtre projet
    project_id = request.GET.get('project')
    if project_id:
        activities = activities.filter(project_id=project_id)

    # 🎯 filtre statut
    status = request.GET.get('status')
    if status:
        activities = activities.filter(status=status)

    projects = Project.objects.all()

    return render(request, 'activities/activity_list.html', {
        'activities': activities,
        'projects': projects
    })


@login_required
def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, user=request.user)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.agent = request.user
            activity.save()
            return redirect('activity_list')
    else:
        form = ActivityForm(user=request.user)

    return render(request, 'activities/activity_form.html', {'form': form})


@login_required
def update_activity(request, id):
    activity = get_object_or_404(Activity, id=id)

    # 🔒 Sécurité : bloquer si pas en attente
    if activity.status != "en_attente":
        messages.error(request, "Impossible de modifier une activité validée.")
        return redirect('activity_list')

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity, user=request.user)

    return render(request, 'activities/activity_form.html', {'form': form})


@login_required
def delete_activity(request, id):
    activity = get_object_or_404(Activity, id=id)

    # 🔒 Sécurité : bloquer si pas en attente
    if activity.status != "en_attente":
        messages.error(request, "Impossible de supprimer une activité validée.")
        return redirect('activity_list')

    activity.delete()
    return redirect('activity_list')


@login_required
def validate_activity(request, id):
    activity = get_object_or_404(Activity, id=id)
    activity.status = 'valide'
    activity.save()
    return redirect('activity_list')


@login_required
def reject_activity(request, id):
    activity = get_object_or_404(Activity, id=id)
    activity.status = 'rejete'
    activity.save()
    return redirect('activity_list')


@login_required
def activity_detail(request, id):
    activity = get_object_or_404(Activity, id=id)

    # 🔐 sécurité
    if not request.user.is_superuser:
        if activity.project not in Project.objects.filter(assigned_agents=request.user):
            return redirect('activity_list')

    return render(request, 'activities/activity_detail.html', {
        'activity': activity
    })

# =========================
# 📊 DASHBOARD RESPONSABLE
# =========================

@login_required
def dashboard(request):

    projects = Project.objects.all()

    return render(request, 'dashboard.html', {
        'projects': projects,
        'total_projects': Project.objects.filter(status='actif').count(),
        'total_beneficiaries': Beneficiary.objects.count(),
        'activities_pending': Activity.objects.filter(status='en_attente').count(),
        'total_activities': Activity.objects.count(),
        'recent_activities': Activity.objects.order_by('-date')[:5],
        'project_data': [
            {
                'name': p.name,
                'count': Beneficiary.objects.filter(project=p).count()
            }
            for p in projects
        ]
    })


# =========================
# 📄 RAPPORTS
# =========================

@login_required
def report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})


@login_required
def create_report(request):

    activity_id = request.GET.get('activity')

    if request.method == 'POST':
        form = ReportForm(request.POST, user=request.user)

        if form.is_valid():
            report = form.save(commit=False)

            # 🔥 sécuriser le lien activité
            if activity_id:
                activity = Activity.objects.get(id=activity_id)
                report.activity = activity
                report.project = activity.project

            report.save()
            return redirect('report_list')

    else:
        # 🔥 Pré-remplissage
        initial_data = {}

        if activity_id:
            try:
                activity = Activity.objects.get(id=activity_id)
                initial_data = {
                    'project': activity.project,
                    'activity': activity,
                }
            except Activity.DoesNotExist:
                pass

        form = ReportForm(initial=initial_data, user=request.user)

    return render(request, 'reports/report_form.html', {'form': form})


@login_required
def report_detail(request, id):
    report = get_object_or_404(Report, id=id)
    return render(request, 'reports/report_detail.html', {'report': report})




@login_required
def export_report_pdf(request, id):
    report = get_object_or_404(Report, id=id)

    template = get_template('reports/report_pdf.html')
    html = template.render({'report': report})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="rapport_{report.id}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response


