from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import Projeto, Tarefa, Equipe, RelationshipEquipe, RelationshipTarefa
from django.contrib.auth.admin import UserAdmin

admin.site.register(Projeto)
admin.site.register(Equipe)
admin.site.register(Tarefa)
admin.site.register(RelationshipEquipe)
admin.site.register(RelationshipTarefa)


