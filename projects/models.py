from django.db import models
from django.contrib.auth.models import User



class Project(models.Model):

    STATUS_CHOICES = [
        ('actif', 'Actif'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    CATEGORY_CHOICES = [
        ('education', 'Éducation'),
        ('sante', 'Santé'),
        ('eau', 'Eau & Assainissement'),
        ('nutrition', 'Nutrition'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(default="Description du projet")

    region = models.CharField(max_length=100, default="Lomé")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='education')

    start_date = models.DateField(default="2024-01-01")
    end_date = models.DateField(default="2024-12-31")

    budget = models.FloatField(default=0)
    progress = models.IntegerField(default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')

    # 🔥 NOUVEAU : agents assignés
    assigned_agents = models.ManyToManyField(User, blank=True, related_name='assigned_projects')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Beneficiary(models.Model):

    GENDER_CHOICES = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='beneficiaries'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField()

    region = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    





class Activity(models.Model):

    TYPE_CHOICES = [
        ('distribution', 'Distribution'),
        ('formation', 'Formation'),
        ('sensibilisation', 'Sensibilisation'),
        ('visite', 'Visite terrain'),
    ]

    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    agent = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    result = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='en_attente'
    )

    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.project.name}"
    

class Report(models.Model):
    title = models.CharField(max_length=255)

    # 🔗 Projet lié
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    # 🔥 NOUVEAU : activité liée
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # 📅 Période
    start_date = models.DateField()
    end_date = models.DateField()

    # 📝 Contenu du rapport
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    # 📌 Statut
    STATUS_CHOICES = [
        ('generated', 'Généré'),
        ('draft', 'Brouillon'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    def __str__(self):
        if self.activity:
            return f"{self.title} - {self.activity}"
        return f"{self.title} - {self.project}"

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generated')

    def __str__(self):
        return self.title