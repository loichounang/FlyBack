# Generated by Django 5.1 on 2024-09-15 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0013_rename_cours_image_cours_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leçon',
            old_name='fichier_détails',
            new_name='fichier_details',
        ),
    ]
