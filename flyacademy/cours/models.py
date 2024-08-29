from django.db import models

class Catégorie(models.Model):
    libellé = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.libellé

class Cours(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    auteur = models.ForeignKey('utilisateurs.Administrateur', on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='cours/fichiers/', null=True, blank=True)
    objectifs = models.TextField()
    durée = models.CharField(max_length=50)
    lien_video = models.URLField(null=True, blank=True)
    catégorie = models.ForeignKey(Catégorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Chapitre(models.Model):
    titre = models.CharField(max_length=255)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Leçon(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='leçons/images/', null=True, blank=True)
    lien_video = models.URLField(null=True, blank=True)
    fichier_détails = models.FileField(upload_to='leçons/fichiers/', null=True, blank=True)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE, blank=True, null=True)

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
