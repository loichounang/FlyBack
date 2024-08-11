# messagerie/serializers.py

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'contenu', 'expéditeur', 'date_envoi', 'destinataire']
