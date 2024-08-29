from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import logging
logger = logging.getLogger(__name__)



# Create your models here. 
class Candidature(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='candidature')
    nom = models.CharField(max_length=50,null=True)
    prenom = models.CharField(max_length=50,null=True)
    email = models.EmailField(max_length=50, null=True)
    cni = models.CharField(max_length=50,null=True)
    telephone=models.CharField(max_length=30)
    localisation = models.CharField(max_length=50,null=True)
    photo = models.ImageField(upload_to='photo')
    cv = models.FileField(upload_to='cv')
    lettre_motivation = models.FileField(upload_to='lettre_motivation')
    OPTION_ONE = 'en attente'
    OPTION_TWO = 'validée'
    OPTION_THREE = 'refusée'

    CHOICES = [
        (OPTION_ONE, 'En attente'),
        (OPTION_TWO, 'Validée'),
        (OPTION_THREE, 'Refusée'),
    ]

    statut = models.CharField(
        max_length=10,
        choices=CHOICES,
        default=OPTION_ONE,
    )

    class Meta:
        verbose_name = ("Candidature")
        verbose_name_plural = ("Candidatures")
        
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
 
class Projet(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    objectif = models.CharField(max_length=50)
    date_debut = models.DateField(verbose_name="Date de début (jj/mm/aaaa)")
    date_fin = models.DateField(verbose_name="Date de fin (jj/mm/aaaa)")
    
    class Meta:
        verbose_name = ("Projet")
        verbose_name_plural = ("Projets")
    def __str__(self):
        return self.nom
    
class Poste(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True)
        
    class Meta:
        verbose_name = ('Poste')
        verbose_name_plural = ('Postes')
            
    def __str__(self):
        return self.nom
    
    
class Affectation(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.PROTECT, null=True)
    candidature = models.ManyToManyField(Candidature, related_name="affectation", blank=False)
    poste = models.ForeignKey(Poste, null=True, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
    
    def __str__(self):
        return f"{self.projet}"