# Generated by Django 5.1 on 2024-08-30 07:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagerie', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='destinataire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinataire', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='expéditeur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expéditeur', to=settings.AUTH_USER_MODEL),
        ),
    ]
