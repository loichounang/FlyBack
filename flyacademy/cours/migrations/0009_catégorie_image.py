# Generated by Django 5.1 on 2024-09-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0008_catégorie_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='catégorie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
