from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Cours, Catégorie, Leçon

@receiver(post_save, sender=Cours)
def update_category_count_on_add(sender, instance, created, **kwargs):
    if created:
        # Incrémente le champ value de la catégorie associée
        instance.categorie.value += 1
        instance.categorie.save()

@receiver(post_delete, sender=Cours)
def update_category_count_on_delete(sender, instance, **kwargs):
    # Décrémente le champ value de la catégorie associée lorsqu'un cours est supprimé
    if instance.categorie.value > 0:
        instance.categorie.value -= 1
        instance.categorie.save()

# Signal pour mettre à jour la durée d'un chapitre et du cours après avoir ajouté ou modifié une leçon
@receiver(post_save, sender=Leçon)
def update_duree_on_lecon_save(sender, instance, **kwargs):
    chapitre = instance.chapitre
    if chapitre:
        chapitre.update_duree()

# Signal pour mettre à jour la durée d'un chapitre et du cours après avoir supprimé une leçon
@receiver(post_delete, sender=Leçon)
def update_duree_on_lecon_delete(sender, instance, **kwargs):
    chapitre = instance.chapitre
    if chapitre:
        chapitre.update_duree()