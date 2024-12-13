# products/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import ChangeLog, Product, Site, Equipment

@receiver(post_save, sender=Product)
def log_product_changes(sender, instance, created, **kwargs):
    # Déterminez le user s'il est connu, sinon None
    # Ici, on ne sait pas forcément qui modifie. Si vous avez l'info, adaptez.
    description = "Création du produit" if created else "Mise à jour du produit"
    ChangeLog.objects.create(
        user=instance.created_by if created else None,
        content_type=ContentType.objects.get_for_model(Product),
        object_id=instance.id,
        change_description=description
    )

@receiver(post_save, sender=Site)
def log_site_changes(sender, instance, created, **kwargs):
    description = "Création du site" if created else "Mise à jour du site"
    ChangeLog.objects.create(
        user=None,  # Adaptez si vous avez un user qui effectue la modif
        content_type=ContentType.objects.get_for_model(Site),
        object_id=instance.id,
        change_description=description
    )

@receiver(post_save, sender=Equipment)
def log_equipment_changes(sender, instance, created, **kwargs):
    description = "Création de l'équipement" if created else "Mise à jour de l'équipement"
    ChangeLog.objects.create(
        user=None,  # Adaptez si vous avez un user
        content_type=ContentType.objects.get_for_model(Equipment),
        object_id=instance.id,
        change_description=description
    )
