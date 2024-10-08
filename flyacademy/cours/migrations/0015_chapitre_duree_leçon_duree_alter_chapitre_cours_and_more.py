# Generated by Django 5.1 on 2024-09-15 04:03

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0014_rename_fichier_détails_leçon_fichier_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapitre',
            name='duree',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='leçon',
            name='duree',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chapitre',
            name='cours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapitres', to='cours.cours'),
        ),
        migrations.AlterField(
            model_name='cours',
            name='duree',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AlterField(
            model_name='leçon',
            name='chapitre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lecons', to='cours.chapitre'),
        ),
    ]
