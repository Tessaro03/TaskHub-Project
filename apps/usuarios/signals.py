from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Relationship

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    
    if created:
        UserProfile.objects.create(user=instance)
        
@receiver(post_save, sender=Relationship)
def post_save_create_relationship(sender, instance, created, **kwargs):
    if instance.status == 'aceito':
        # Verifica se já existe um relacionamento reverso (receiver -> sender)
        if not Relationship.objects.filter(sender=instance.receiver, receiver=instance.sender, status='aceito').exists():
            Relationship.objects.create(sender=instance.receiver, receiver=instance.sender, status='aceito')

    if instance.status == 'recusado':
        # Exclui relacionamento reverso se existir
        Relationship.objects.filter(sender=instance.receiver, receiver=instance.sender, status='aceito').delete()


        