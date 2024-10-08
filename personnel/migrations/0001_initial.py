# Generated by Django 5.1 on 2024-08-29 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Poste',
                'verbose_name_plural': 'Postes',
            },
        ),
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('objectif', models.CharField(max_length=50)),
                ('date_debut', models.DateField(verbose_name='Date de début (jj/mm/aaaa)')),
                ('date_fin', models.DateField(verbose_name='Date de fin (jj/mm/aaaa)')),
            ],
            options={
                'verbose_name': 'Projet',
                'verbose_name_plural': 'Projets',
            },
        ),
        migrations.CreateModel(
            name='Candidature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, null=True)),
                ('prenom', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('cni', models.CharField(max_length=50, null=True)),
                ('telephone', models.CharField(max_length=30)),
                ('localisation', models.CharField(max_length=50, null=True)),
                ('photo', models.ImageField(upload_to='photo')),
                ('cv', models.FileField(upload_to='cv')),
                ('lettre_motivation', models.FileField(upload_to='lettre_motivation')),
                ('statut', models.CharField(choices=[('en attente', 'En attente'), ('validée', 'Validée'), ('refusée', 'Refusée')], default='en attente', max_length=10)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidature', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Candidature',
                'verbose_name_plural': 'Candidatures',
            },
        ),
        migrations.CreateModel(
            name='Affectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidature', models.ManyToManyField(related_name='affectation', to='personnel.candidature')),
                ('poste', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='personnel.poste')),
                ('projet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='personnel.projet')),
            ],
            options={
                'verbose_name': 'Affectation',
                'verbose_name_plural': 'Affectations',
            },
        ),
    ]
