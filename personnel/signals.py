import logging
from mds import settings 
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from personnel.models import Affectation, Candidature
from django.utils.dateformat import format

import logging

logger = logging.getLogger(__name__)

            
@receiver(m2m_changed, sender=Affectation.candidature.through)
def envoyer_email_apres_enregistrement(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        # if pk_set:
            date_debut = format(instance.projet.date_debut, 'd/m/Y')
            date_fin = format(instance.projet.date_fin, 'd/m/Y') 
            candidatures = Candidature.objects.filter(pk__in=pk_set)
            logger.info(f'Nombre de candidatures : {candidatures.count()}')  
            for candidature in candidatures:
                sujet = 'Nouvelle affectation'
                message = f'Bonjour {candidature.nom},\n\nVous avez été affecté au projet {instance.projet.nom} pour le poste de {instance.poste.nom} allant du {date_debut} au {date_fin}.'
                destinataire = [candidature.email]
                email = EmailMessage(
                    sujet, message, settings.EMAIL_HOST_USER, destinataire,
                )
                email.fail_silently = False
                try:
                    email.send()
                    logger.info(f'Email envoyé à {candidature.email}')
                except Exception as e:
                    logger.error(f'Erreur lors de l\'envoi de l\'email à {candidature.email}: {e}')
                    print(f'Erreur lors de l\'envoi de l\'email à {candidature.email}: {e}')
    else:
        if action == "post_remove":
             candidatures = Candidature.objects.filter(pk__in=pk_set)
             logger.info(f'Nombre de candidatures : {candidatures.count()}')  
             for candidature in candidatures:
                 sujet = "retrait d'affectation"
                 message = f'Bonjour {candidature.nom},\n\nVous avez été retiré du projet {instance.projet.nom} pour le poste de {instance.poste.nom}.'
                 destinataire = [candidature.email]
                 email = EmailMessage(
                    sujet, message, settings.EMAIL_HOST_USER, destinataire,
                 )
                 email.fail_silently = False
                 try:
                     email.send()
                     logger.info(f'Email envoyé à {candidature.email}')
                 except Exception as e:
                     logger.error(f'Erreur lors de l\'envoi de l\'email à {candidature.email}: {e}')
                     print(f'Erreur lors de l\'envoi de l\'email à {candidature.email}: {e}')
                 
            
             
            
            
    
   
