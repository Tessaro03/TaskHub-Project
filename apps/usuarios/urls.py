from django.urls import path
from usuarios.views import *


urlpatterns = [
    path("perfil/<str:amigo_id>", perfil, name='perfil'),
    path('remover/<int:amigo_id>',removerAmigo ,name="removerAmigo"),
    path('adiconar/<int:amigo_id>', adicionarAmigo ,name="adicionarAmigo"),
    path("login", login, name='login'),
    path("cadastrar-se", cadastro, name='cadastro'),
    path("cadastro/perfil", userProfile, name='userProfile'),
    path("logout", logout, name='logout'),
    path('usuarios', buscaUsuarios, name='usuario'),
]    

