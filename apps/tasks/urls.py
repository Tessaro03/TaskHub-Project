from django.urls import path
from tasks.views import *

urlpatterns = [
    path("",inicial, name='inicial'),
    path("home", index, name='home'),
    path('filtro/<str:filtro>/<str:valor>/', index, name='filtro'),
    path('buscar',buscar,name='buscar'),
    path('criar/projeto',criarProjeto ,name="criarProjeto"),
    path('novo_projeto',novo_projeto, name='novo_projeto'),
    path('criar/tarefa/<int:projeto_id>',criarTarefa ,name="criarTarefa"),
    path('novo_tarefa/<int:projeto_id>',novo_tarefa, name='novo_tarefa'),
    path('notificações',notificacao ,name="notificações"),
    path('atualizar_status/<str:relacionamento>/<int:notificacao_id>/<str:status>/',atualizar_status, name='atualizar_status'),
    path('convidar/equipe/<int:projeto_id>',convidaEquipe ,name="convidaEquipe"),
    path('remover_equipe/<int:amigo_id>/<int:projeto_id>', removerEquipe, name='remover_equipe'),
    path('cancelar_convite/<int:convite_id>/<int:projeto_id>', cancelarConvite, name='cancelar_convite'),
    path('convidar_amigo/<int:amigo_id>/<int:projeto_id>', convidarAmigo, name='convidar_amigo'),
    path("projeto/<int:projeto_id>", projeto, name='projeto'),
    path('editar/projeto/<int:projeto_id>',editar_projeto ,name="editar_projeto"),
    path('editar/tarefa/<int:tarefa_id>/<int:projeto_id>', editar_tarefa ,name="editar_tarefa"),
    path('excluir/projeto/<int:projeto_id>', excluirProjeto , name='excluirProjeto'),
    path('excluir/tarefa/<int:tarefa_id>/<int:projeto_id>', excluirTarefa , name='excluirTarefa'),
    path('adicionar/<int:projeto_id>/<int:tarefa_id>',MembrosTarefa, name='MembrosTarefa'),
    path('adicionar/equipe/<int:projeto_id>/<int:usuario_id>/<int:tarefa_id>', addMembroTarefa, name='addMembroTarefa'),
    path('remover/equipe/<int:projeto_id>/<int:usuario_id>/<int:tarefa_id>', popMembroTarefa, name='popMembroTarefa'),
]

