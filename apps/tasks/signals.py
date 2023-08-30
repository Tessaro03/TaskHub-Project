from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Projeto, Equipe, RelationshipEquipe


@receiver(post_save, sender=Projeto)
def post_save_create_equipe(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.get(user=instance.usuario)
        Equipe.objects.create(projeto=instance, usuario=user_profile)

@receiver(post_save, sender=RelationshipEquipe)
def post_save_add_to_equipe(sender, instance, created, **kwargs):
    projeto = instance.projeto
    convidado = instance.convidado        
    if instance.status == 'aceito':
        equipe = Equipe.objects.create(projeto=projeto, usuario=convidado)
    elif instance.status == 'recusado':
        instance.delete()

