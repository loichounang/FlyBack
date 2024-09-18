# utilisateurs/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        if not password:
            raise ValueError("Le mot de passe est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('administrateur', 'Administrateur'),
        ('ambassadeur', 'Ambassadeur'),
        ('team_leader', "Leader"),
    )

    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    prénom = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ambassadeur')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    dernier_accès = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, default='actif')
    date_joined = models.DateField(auto_now_add=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prénom']

    objects = UtilisateurManager()

    def __str__(self):
        return f'{self.nom} {self.prénom}'

    def has_perm(self, perm, obj=None):
        # Permissions spécifiques selon le rôle
        if self.role == 'administrateur':
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        # Permet l'accès aux modules pour les administrateurs
        if self.role == 'administrateur':
            return True
        return super().has_module_perms(app_label)
