from django.db import models
from utilisateurs.models import Utilisateur
from django.conf import settings
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cours = models.ForeignKey('Cours', related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Note de 1 à 5 étoiles
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cours')  # Un utilisateur ne peut évaluer un cours qu'une seule fois

    def __str__(self):
        return f"{self.user} - {self.cours} - {self.score}"

class Catégorie(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    value = models.IntegerField(default=0)  # Nouveau champ pour compter les cours
    image = models.ImageField(null=True, blank=True)
    # Ajouter d'autres champs si besoin...

    def __str__(self):
        return self.name

class Cours(models.Model):
    STATUS_CHOICES = [
        ('active', 'Démarré'),
        ('inactive', 'Pas encore commencé'),
    ]
    titre = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'administrateur'},
        related_name='cours'
    )
    fichier = models.FileField(upload_to='cours/fichiers/', null=True, blank=True)
    objectifs = models.TextField()
    duree = models.DurationField(default=timedelta())  # Mis à jour automatiquement
    lien_video = models.URLField(null=True, blank=True)
    categorie = models.ForeignKey(Catégorie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cours/images/', null=True, blank=True)
    cours_status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='inactive')

    # Champs pour le système de notation
    average_rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.titre

    def update_rating(self):
        ratings = self.ratings.all()
        self.rating_count = ratings.count()
        if self.rating_count > 0:
            self.average_rating = sum([rating.score for rating in ratings]) / self.rating_count
        else:
            self.average_rating = 0.0
        self.save()

    def update_duree(self):
        # Mettre à jour la durée du cours basée sur les chapitres
        total_duree = timedelta()

        # Parcourir chaque chapitre et additionner les durées
        for chapitre in self.chapitres.all():
            if chapitre.duree:
                total_duree += chapitre.duree
    
        # Convertir total_duree en un format approprié pour le champ `duree`
        self.duree = str(total_duree)  # Ajustez en fonction du format attendu pour le champ `duree`

        self.save()

class CoursUtilisateur(models.Model):
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE)
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
    date_début = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=25,
        choices=[
            ('active', 'Actif'),
            ('completed', 'Terminé'),
            ('dropped', 'Abandonné'),
        ],
        default='active'
    )

    def __str__(self):
        return f"{self.utilisateur} - {self.cours} ({self.statut})"
    
class ProgressionLeçon(models.Model):
    cours_utilisateur = models.ForeignKey(CoursUtilisateur, on_delete=models.CASCADE, related_name='progressions')
    leçon = models.ForeignKey('Leçon', on_delete=models.CASCADE)
    statut_leçon = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Non commencée'),
            ('in_progress', 'En cours'),
            ('completed', 'Terminée'),
        ],
        default='not_started'
    )
    date_terminée = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cours_utilisateur.utilisateur} - {self.leçon} ({self.statut_leçon})"
    
class Chapitre(models.Model):
    titre = models.CharField(max_length=255)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='chapitres')
    duree = models.DurationField(default=timedelta())  # Mis à jour automatiquement

    def __str__(self):
        return self.titre

    def update_duree(self):
        total_seconds = 0
        for lecon in self.lecons.all():
            if lecon.duree:
                # Convertir la durée en secondes pour le calcul
                if isinstance(lecon.duree, timedelta):
                    total_seconds += lecon.duree.total_seconds()
                else:
                    # Vous pouvez avoir un champ `duree` sous forme de chaîne ou d'entier,
                    # assurez-vous qu'il est correctement converti en timedelta si nécessaire.
                    try:
                        # Assumer `duree` est en minutes ou heures, ajustez selon vos besoins
                        duration_parts = lecon.duree.split(':')  # par exemple "01:30:00"
                        duration_timedelta = timedelta(
                            hours=int(duration_parts[0]),
                            minutes=int(duration_parts[1]),
                            seconds=int(duration_parts[2])
                        )
                        total_seconds += duration_timedelta.total_seconds()
                    except ValueError:
                        continue  # Ignorer les durées invalides
        
        # Convertir le total des secondes en timedelta pour stocker dans le modèle
        self.duree = timedelta(seconds=total_seconds)
        self.save()

        # Mettre à jour la durée du cours parent
        self.cours.update_duree()


class Leçon(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='leçons/images/', null=True, blank=True)
    lien_video = models.URLField(null=True, blank=True)
    fichier_details = models.FileField(upload_to='leçons/fichiers/', null=True, blank=True)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE, blank=True, null=True, related_name='lecons')
    duree = models.DurationField(blank=True, null=True)  # Durée définie manuellement

    def __str__(self):
        return self.titre

class Quizz(models.Model):
    question = models.TextField()
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)

    def __str__(self):
        return f'Quizz: {self.question}'

class OptionQuizz(models.Model):
    texte_option = models.CharField(max_length=255)
    est_correct = models.BooleanField(default=False)
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)

    def __str__(self):
        return self.texte_option
