# Generated by Django 5.1 on 2024-08-29 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leçon',
            name='chapitre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cours.chapitre'),
        ),
    ]
