from django.contrib.auth.models import User
from django.db import models
from usuarios.models import UserProfile




STATUS_PROJETO = (
    ('Razoável','Razoável'),
    ('Médio','Médio'),
    ('Alto','Alto'),
)
COR_PROJETO = (
    ('#ff7a7a','Vermelho'),
    ('#fed148','Amarelo'),
    ('#92fc8d','Verde'),
    ('#55adfb','Azul'),
    ('#f592fa','Roxo'),
    ('#cc7aff','Rosa'),
    ('#ffffff','Branco'),
)


class Projeto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=200)
    cor = models.CharField(max_length=8, choices=COR_PROJETO, default=None)
    status = models.CharField(max_length=8, choices=STATUS_PROJETO, default=None)
    data_inicio = models.DateField(default=None)
    data_termino = models.DateField(default=None)
    

    def __str__(self):
        return self.titulo

class Equipe(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Equipe {self.usuario}'


class Tarefa(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateField(default=None)
    data_termino = models.DateField(default=None)
    completa = models.BooleanField(default=False)
    def __str__(self):
        return self.titulo
    
STATUS_CHOICES = (
    ('enviado','Enviado'),
    ('aceito','Aceito'),
    ('recusado','Recusado')
)

class RelationshipEquipe(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='usuario', default=None)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='projetos', default=None)
    convidado = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='convidado')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self): 
        return f'{self.projeto}-{self.convidado}-{self.status}'
    
class RelationshipTarefa(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='usuario_tarefa', default=None)
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='tarefas', default=None)

    def __str__(self): 
        return f'{self.tarefa}-{self.usuario}'
    