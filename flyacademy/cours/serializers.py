# cours/serializers.py

from rest_framework import serializers
from .models import Catégorie, Cours, Chapitre, Leçon, Quizz

class CatégorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catégorie
        fields = ['id', 'libellé', 'description']

class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = ['id', 'titre', 'description', 'auteur', 'fichier', 'objectifs', 'durée', 'lien_video', 'catégorie']

class ChapitreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = ['id', 'titre', 'cours']

class LeçonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leçon
        fields = ['id', 'titre', 'description', 'image', 'lien_video', 'fichier_détails', 'chapitre']

class QuizzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizz
        fields = ['id', 'question', 'chapitre']
