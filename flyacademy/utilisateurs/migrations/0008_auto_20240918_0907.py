from django.db import migrations
from django.conf import settings
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    # Récupérer le modèle Utilisateur personnalisé
    User = get_user_model()
    
    # Créer un super utilisateur avec tous les champs requis
    User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword',
        nom='Admin',
        prénom='Administrateur',
        role='administrateur',
    )

class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0007_alter_utilisateur_role'),  # Mettre à jour en fonction de votre dernière migration correcte
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
