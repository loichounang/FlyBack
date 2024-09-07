from django.db import models
from utilisateurs.models import Utilisateur

class Message(models.Model):
    expéditeur = models.ForeignKey(Utilisateur, related_name='expéditeur', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Utilisateur, related_name='destinataire', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    read_or_not = models.BooleanField(default=False)

    def __str__(self):
        return f'Message de {self.expéditeur} à {self.destinataire}'
