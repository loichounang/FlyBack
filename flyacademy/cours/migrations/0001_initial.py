# Generated by Django 5.1 on 2024-08-11 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catégorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libellé', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('fichier', models.FileField(blank=True, null=True, upload_to='cours/fichiers/')),
                ('objectifs', models.TextField()),
                ('durée', models.CharField(max_length=50)),
                ('lien_video', models.URLField(blank=True, null=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateurs.administrateur')),
                ('catégorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.catégorie')),
            ],
        ),
        migrations.CreateModel(
            name='Chapitre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.cours')),
            ],
        ),
        migrations.CreateModel(
            name='Leçon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='leçons/images/')),
                ('lien_video', models.URLField(blank=True, null=True)),
                ('fichier_détails', models.FileField(blank=True, null=True, upload_to='leçons/fichiers/')),
                ('chapitre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.chapitre')),
            ],
        ),
        migrations.CreateModel(
            name='Quizz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('chapitre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.chapitre')),
            ],
        ),
        migrations.CreateModel(
            name='OptionQuizz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texte_option', models.CharField(max_length=255)),
                ('est_correct', models.BooleanField(default=False)),
                ('quizz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.quizz')),
            ],
        ),
    ]
