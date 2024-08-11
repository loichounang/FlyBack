# utilisateurs/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        if not password:
            raise ValueError('Le mot de passe est obligatoire')
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
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    prénom = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    dernier_accès = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, default='actif')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prénom']

    objects = UtilisateurManager()

    def __str__(self):
        return f'{self.nom} {self.prénom}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Administrateur(Utilisateur):
    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"

    def save(self, *args, **kwargs):
        # Assurez-vous que is_staff et is_superuser sont True pour les Administrateurs
        self.is_staff = True
        self.is_superuser = True
        super().save(*args, **kwargs)

class Ambassadeur(Utilisateur):
    équipe = models.ForeignKey('equipes.Equipe', on_delete=models.SET_NULL, null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ambassadeur"
        verbose_name_plural = "Ambassadeurs"
