from django.db import models
from utilisateurs.models import Utilisateur
from cours.models import Cours, Catégorie, Chapitre, CoursUtilisateur, Leçon
from utilisateurs.models import Utilisateur
from equipes.models import Equipe
from messagerie.models import Message

class Progression(models.Model):
    ambassadeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, default='Non commencé')
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.ambassadeur} - {self.cours} - {self.statut}'
    
class Interactions(models.Model):
    TYPE_CHOICES = [
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
        ('view_course', 'Consultation de Cours'),
        ('complete_course', 'Cours Terminé'),
        ('download_content', 'Téléchargement de Contenu'),
        ('message_sent', 'Message Envoyé'),
        ('search', 'Recherche'),
        # Ajouter d'autres actions si besoin
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.DO_NOTHING)
    type_interaction = models.CharField(max_length=100, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True) # Pour stocker des infos supplémentaires

    def __str__(self):
        return f'{self.utilisateur} - {self.type_interaction} - {self.timestamp}'
