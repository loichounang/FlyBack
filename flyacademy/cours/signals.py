from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Cours, Catégorie

@receiver(post_save, sender=Cours)
def update_category_count_on_add(sender, instance, created, **kwargs):
    if created:
        # Incrémente le champ value de la catégorie associée
        instance.catégorie.value += 1
        instance.catégorie.save()

@receiver(post_delete, sender=Cours)
def update_category_count_on_delete(sender, instance, **kwargs):
    # Décrémente le champ value de la catégorie associée lorsqu'un cours est supprimé
    if instance.catégorie.value > 0:
        instance.catégorie.value -= 1
        instance.catégorie.save()