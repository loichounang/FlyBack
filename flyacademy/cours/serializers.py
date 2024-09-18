# cours/serializers.py

from rest_framework import serializers
from .models import Catégorie, Cours, Chapitre, Leçon, Quizz, Rating, CoursUtilisateur, ProgressionLeçon

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'cours', 'score']

class CatégorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catégorie
        fields = ['id', 'name', 'description', 'image']

class CatégorieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catégorie
        fields = ['id', 'name', 'description', 'value', 'image']

class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = [
            'id', 'titre', 'description', 'auteur', 'fichier',
            'objectifs', 'duree', 'lien_video', 'categorie',
            'image', "average_rating", "rating_count"
        ]

class ChapitreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = ['id', 'titre', 'cours', 'duree']

class LeçonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leçon
        fields = '__all__'
    
    def create(self, validated_data):
        # Personnalisez la méthode create si nécessaire
        # Assurez-vous de traiter les fichiers et autres champs correctement

        # Créez une nouvelle instance de Leçon
        instance = Leçon.objects.create(**validated_data)

        # Vous pouvez ajouter des opérations supplémentaires si nécessaire

        return instance

    def to_representation(self, instance):
        # Personnalisez la représentation si nécessaire, par exemple, pour les durées
        representation = super().to_representation(instance)
        
        # Ajoutez des traitements spécifiques si vous avez des champs comme 'duree' que vous devez manipuler
        if 'duree' in representation:
            # Exemple de formatage pour le champ 'duree'
            representation['duree'] = str(instance.duree)  # Ajustez selon le format de votre champ de durée
        
        return representation

class QuizzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizz
        fields = ['id', 'question', 'chapitre']

class CoursUtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursUtilisateur
        fields = '__all__'

class ProgressionLeçonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressionLeçon
        fields = '__all__'