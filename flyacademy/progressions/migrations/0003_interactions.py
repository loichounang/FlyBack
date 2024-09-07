# Generated by Django 5.1 on 2024-09-02 15:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressions', '0002_alter_progression_ambassadeur'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_interaction', models.CharField(choices=[('login', 'Connexion'), ('logout', 'Déconnexion'), ('view_course', 'Consultation de Cours'), ('complete_course', 'Cours Terminé'), ('download_content', 'Téléchargement de Contenu'), ('message_sent', 'Message Envoyé'), ('search', 'Recherche')], max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('details', models.JSONField(blank=True, null=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
