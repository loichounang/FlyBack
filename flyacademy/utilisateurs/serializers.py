# utilisateurs/serializers.py

from rest_framework import serializers
from .models import Administrateur, Ambassadeur
from equipes.models import Equipe

class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Administrateur  # Utilisez le modèle de base ici si vous souhaitez un serializer général
        fields = ['email', 'nom', 'prénom', 'password', 'dernier_accès', 'statut', 'username']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Administrateur.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['id', 'nom', 'description']  # Ajustez selon vos besoins

class AmbassadeurSerializer(UtilisateurSerializer):
    équipe = EquipeSerializer(read_only=True)  # Utiliser le sérialiseur pour afficher les détails de l'équipe
    date_inscription = serializers.DateTimeField(read_only=True)
    dernier_accès = serializers.DateTimeField(required=False, allow_null=True)
    statut = serializers.CharField(max_length=50, default='inactif')

    class Meta(UtilisateurSerializer.Meta):
        model = Ambassadeur
        fields = UtilisateurSerializer.Meta.fields + ['équipe', 'date_inscription']

class AdministrateurSerializer(UtilisateurSerializer):
    class Meta(UtilisateurSerializer.Meta):
        model = Administrateur
