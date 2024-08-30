# utilisateurs/serializers.py

from rest_framework import serializers
from .models import Utilisateur
from equipes.models import Equipe


class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prénom', 'password', 'dernier_accès', 'statut', 'username', 'role']

    def create(self, validated_data):
        # Extrait et supprime le mot de passe du dictionnaire des données validées
        password = validated_data.pop('password')
        # Crée un nouvel utilisateur avec les données restantes
        user = Utilisateur.objects.create(**validated_data)
        # Définit le mot de passe de l'utilisateur
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # Met à jour les champs de l'instance utilisateur
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['id', 'nom', 'description']


class AmbassadeurSerializer(UtilisateurSerializer):
    équipe = EquipeSerializer(read_only=True)
    date_inscription = serializers.DateTimeField(read_only=True)

    class Meta(UtilisateurSerializer.Meta):
        model = Utilisateur
        fields = UtilisateurSerializer.Meta.fields + ['équipe', 'date_inscription']
        extra_kwargs = {'role': {'default': 'ambassadeur', 'read_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'ambassadeur'  # Définit le rôle automatiquement
        return super().create(validated_data)


class AdministrateurSerializer(UtilisateurSerializer):
    class Meta(UtilisateurSerializer.Meta):
        model = Utilisateur
        extra_kwargs = {'role': {'default': 'administrateur', 'read_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'administrateur'  # Définit le rôle automatiquement
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['email', 'password']
