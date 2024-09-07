# Enregistrement des intéractions sur les actions des utilisateurs

from django.db.models.signals import post_save, post_migrate, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import Interactions

@receiver(user_logged_in)
def log_user_login(sender, user, request, **kwargs):
    Interactions.objects.create(utilisateur=user, type_interaction='login')

@receiver(user_logged_out)
def log_user_logout(sender, user, request, **kwargs):
    Interactions.objects.create(utilisateur=user, type_interaction='logout')