from django.db import models

class Progression(models.Model):
    ambassadeur = models.ForeignKey('utilisateurs.Ambassadeur', on_delete=models.CASCADE)
    cours = models.ForeignKey('cours.Cours', on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, default='Non commencé')
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.ambassadeur} - {self.cours} - {self.statut}'
