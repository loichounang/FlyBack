# Generated by Django 5.1 on 2024-08-31 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagerie', '0002_alter_message_destinataire_alter_message_expéditeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_or_not',
            field=models.BooleanField(default=False),
        ),
    ]
