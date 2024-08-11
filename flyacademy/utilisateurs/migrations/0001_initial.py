# Generated by Django 5.1 on 2024-08-11 05:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('prénom', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Administrateur',
                'verbose_name_plural': 'Administrateurs',
            },
            bases=('utilisateurs.utilisateur',),
        ),
        migrations.CreateModel(
            name='Ambassadeur',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('dernier_accès', models.DateTimeField(blank=True, null=True)),
                ('statut', models.CharField(default='actif', max_length=50)),
                ('équipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipes.équipe')),
            ],
            options={
                'verbose_name': 'Ambassadeur',
                'verbose_name_plural': 'Ambassadeurs',
            },
            bases=('utilisateurs.utilisateur',),
        ),
    ]
