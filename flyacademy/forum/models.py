from django.db import models

class SujetForum(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    auteur = models.ForeignKey('utilisateurs.Ambassadeur', on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class MessageForum(models.Model):
    contenu = models.TextField()
    auteur = models.ForeignKey('utilisateurs.Ambassadeur', on_delete=models.CASCADE)
    sujet = models.ForeignKey(SujetForum, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message de {self.auteur} dans {self.sujet}'
