# forum/serializers.py

from rest_framework import serializers
from .models import SujetForum, MessageForum

class SujetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SujetForum
        fields = ['id', 'titre', 'description', 'auteur', 'date_publication']

class RéponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageForum
        fields = ['id', 'contenu', 'auteur', 'date_publication', 'sujet']
