from rest_framework import serializers
from .models import Equipe

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['nom', 'description']