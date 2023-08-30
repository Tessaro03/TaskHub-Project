from django.contrib.auth.models import User
from django.db import models
import os


upload_to = 'avatar'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='')
    sobrenome = models.CharField(max_length=100, default='')
    empresa = models.CharField(max_length=100, default='')
    avatar = models.FileField(upload_to=upload_to, default='', blank=True)
    

    def __str__(self):
        return self.user.username
    
STATUS_CHOICES = (
    ('enviado','Enviado'),
    ('aceito','Aceito'),
    ('recusado','Recusado')
)

class Relationship(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self): 
        return f'{self.sender}-{self.receiver}-{self.status}'
    

    