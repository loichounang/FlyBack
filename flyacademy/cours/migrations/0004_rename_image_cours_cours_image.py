# Generated by Django 5.1 on 2024-08-31 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0003_cours_image_alter_cours_auteur'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cours',
            old_name='image',
            new_name='cours_image',
        ),
    ]
