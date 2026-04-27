from django import forms
from django.contrib.auth.models import User
from .models import Project, Beneficiary, Activity, Report


# =========================
# 📋 PROJECT FORM (PROPRE)
# =========================

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'category',
            'region',
            'start_date',
            'end_date',
            'budget',
            'status',
            'progress'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),

            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),

            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# =========================
# 👥 BENEFICIARY
# =========================

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['first_name', 'last_name', 'gender', 'age', 'region', 'project']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['project'].queryset = Project.objects.all()


# =========================
# 📊 ACTIVITY
# =========================

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['project', 'type', 'description', 'result']

        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'result': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 🔥 Filtrer projets
        if user:
            self.fields['project'].queryset = Project.objects.filter(
                assigned_agents=user
            )

        # 🔥 MASQUER RESULT À LA CRÉATION
        if not self.instance or not self.instance.pk:
            self.fields['result'].widget = forms.HiddenInput()

        # 🔥 AFFICHER RESULT SEULEMENT SI ACTIVITÉ VALIDÉE
        elif self.instance.status != "valide":
            self.fields['result'].widget = forms.HiddenInput()


            
# =========================
# 📄 REPORT
# =========================

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'project', 'activity', 'start_date', 'end_date', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'activity': forms.Select(attrs={'class': 'form-select'}),

            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # 🔥 AGENT → seulement ses activités validées
            if not user.is_superuser:
                self.fields['activity'].queryset = Activity.objects.filter(
                    agent=user,
                    status='valide'
                )
                self.fields['project'].queryset = Project.objects.filter(
                    assigned_agents=user
                )
            else:
                # 🔥 RESPONSABLE → voit tout
                self.fields['activity'].queryset = Activity.objects.all()
                self.fields['project'].queryset = Project.objects.all()


# =========================
# 👥 ASSIGN AGENT
# =========================

class AssignAgentForm(forms.ModelForm):
    assigned_agents = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=False),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['assigned_agents']