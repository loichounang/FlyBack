from django.db import models

class Message(models.Model):
    expéditeur = models.ForeignKey('utilisateurs.Ambassadeur', related_name='expéditeur', on_delete=models.CASCADE)
    destinataire = models.ForeignKey('utilisateurs.Ambassadeur', related_name='destinataire', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message de {self.expéditeur} à {self.destinataire}'
