from django.shortcuts import render, redirect , get_object_or_404
from .models import *
from usuarios.models import Relationship
from django.contrib.auth.decorators import login_required
from tasks.forms import ProjetoForm, TarefaForm
from django.contrib import messages


def inicial(request):
    return render(request, "tasks/home.html")


@login_required(login_url='login')
def index(request, filtro=None, valor=None):
    '''Pagina Principal. com Filtros e Informações dos Projetos'''
    user_profile = request.user.userprofile
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    usuario = UserProfile.objects.filter(user=request.user)
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    if filtro == 'cor':
        projetos = Projeto.objects.filter(equipe__usuario=user_profile, cor=valor).order_by('data_termino')
    elif filtro == 'status':
        projetos = Projeto.objects.filter(equipe__usuario=user_profile, status=valor).order_by('data_termino')
    else:
        projetos = Projeto.objects.filter(equipe__usuario=user_profile).order_by('data_termino')
    projetos_com_porcentagem = []
    for projeto in projetos:
        tarefas_completas = Tarefa.objects.filter(projeto=projeto, completa=True).count()
        total_tarefas = Tarefa.objects.filter(projeto=projeto).count()
        porcentagem = int((tarefas_completas / total_tarefas) * 100) if total_tarefas > 0 else 0
        equipe = Equipe.objects.filter(projeto=projeto)
        projetos_com_porcentagem.append((projeto, tarefas_completas, porcentagem, equipe))
    return render(request, 'tasks/tasks.html', 
                {'projetos_com_porcentagem': projetos_com_porcentagem,
                'projetos':todosProjetos,'usuario':usuario, 'notificacao':notificacao })

@login_required(login_url='login')
def buscar(request):
    '''Função de Busca por nome de Projeto'''
    user_profile = request.user.userprofile
    projetos = Projeto.objects.filter(equipe__usuario=user_profile).order_by('data_termino')
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    projetos_com_porcentagem = []
    usuario = UserProfile.objects.filter(user=request.user)
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    if "buscar" in request.GET:
            nome_buscar = request.GET['buscar']
            if nome_buscar:
                projetos = projetos.filter(equipe__usuario=user_profile, titulo__icontains=nome_buscar)   
                for projeto in projetos:
                    tarefas_completas = Tarefa.objects.filter(projeto=projeto, completa=True).count()
                    total_tarefas = Tarefa.objects.filter(projeto=projeto).count()
                    porcentagem = int((tarefas_completas / total_tarefas) * 100) if total_tarefas > 0 else 0
                    equipe = Equipe.objects.filter(projeto=projeto)
                    
                    projetos_com_porcentagem.append((projeto, tarefas_completas, porcentagem, equipe))
        
    return render(request, 'tasks/tasks.html', 
                  {'projetos_com_porcentagem': projetos_com_porcentagem,'notificacao':notificacao,
                    'projetos':todosProjetos,'usuario':usuario})

@login_required(login_url='login')
def projeto(request,projeto_id):
    '''Pagina do Projeto'''
    user_profile = request.user.userprofile
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    projeto = get_object_or_404(Projeto, id=projeto_id)
    tarefas = Tarefa.objects.filter(projeto=projeto_id).order_by('data_termino')
    tarefas_completas = Tarefa.objects.filter(projeto=projeto_id, completa=True).count()
    total_tarefas = Tarefa.objects.filter(projeto=projeto_id).count()
    equipe = Equipe.objects.filter(projeto=projeto_id)

    if faz_parte_equipe(equipe, user_profile.id) == False:
        print(equipe,user_profile.id)
        return redirect('home')

    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    usuarioTarefa = RelationshipTarefa.objects.filter(tarefa__projeto=projeto_id)
    return render(request,'tasks/projeto.html',
                   {'projeto':projeto, 'projetos':todosProjetos,'tarefas':tarefas, 
                    'tarefas_completas':tarefas_completas, 'total_tarefas':total_tarefas,
                    'equipe':equipe, 'notificacao':notificacao, 'usuarioTarefa': usuarioTarefa})

# ------------------- Criar Projeto ----------------------

@login_required(login_url='login')
def criarProjeto(request):
    ''' Pagina de Criação de Projeto'''
    user_profile = request.user.userprofile
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    projeto = ProjetoForm
    usuario = UserProfile.objects.filter(user=request.user)
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    return render(request, 'tasks/projetoCreate.html' ,
                  {'form':projeto,'projetos':todosProjetos,'usuario':usuario,
                   'projeto_id':000, 'notificacao':notificacao})

@login_required(login_url='login')
def novo_projeto(request):
    ''' Criação de Projeto '''
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ProjetoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            projeto_id = form.instance.id
            return redirect('criarTarefa', projeto_id)
    else:
        form = ProjetoForm(user=request.user)
    return redirect('criarProjeto')

# ------------------- Criar Tarefa ----------------------

@login_required(login_url='login')
def criarTarefa(request, projeto_id=None):
    '''Pagina de Criação de Tarefa'''
    user_profile = request.user.userprofile
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    ultimo_projeto = Projeto.objects.filter(usuario=request.user).latest('id')
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    if projeto_id is not None:
        projeto = get_object_or_404(Projeto, id=projeto_id, equipe__usuario=user_profile)
        tarefa = TarefaForm(initial={'projeto': projeto})
        return render(request, 'tasks/tarefaCreate.html',
                   {'form': tarefa, 'projetos': todosProjetos,
                    'tarefa_id':000, 'notificacao':notificacao, 'projeto_id':projeto_id})
    else:
        tarefa = TarefaForm(initial={'projeto': ultimo_projeto})
   
    return render(request, 'tasks/tarefaCreate.html',
                   {'form': tarefa, 'projetos': todosProjetos,
                    'tarefa_id':000, 'notificacao':notificacao})

@login_required(login_url='login')
def novo_tarefa(request, projeto_id):
    '''Criação de Tarefa'''
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Tarefa Criada!")
            return redirect('projeto', projeto_id)
    else:
        form = ProjetoForm(user=request.user)
    return redirect('criarTarefa', projeto_id)


# ------------------- Notificações ----------------------


@login_required(login_url='login')
def notificacao(request):
    '''Notificações de Projetos e Amizidades'''
    user_profile = request.user.userprofile
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    return render(request, 'usuarios/notificacao.html', 
                  { 'projetos':todosProjetos,'notificacaoAmigo': notificacaoAmigo,
                   'notificacaoEquipe': notificacaoEquipe,'notificacao':notificacao })

@login_required(login_url='login')
def atualizar_status(request, relacionamento, notificacao_id, status):
    ''' Escolha de Notificação - AMIZADA ou PROJETO (Recusar ou Aceitar)'''
    if relacionamento == 'relationship':
        notificacao = get_object_or_404(Relationship, id=notificacao_id)
        if status == 'aceito' or 'recusado':
            notificacao.status = status
            notificacao.save()

    elif relacionamento == 'relationship_equipe':
        notificacao = get_object_or_404(RelationshipEquipe, id=notificacao_id)
        if status == 'aceito' or 'recusado':
            notificacao.status = status 
            notificacao.save()
    else:
        return redirect('notificações')
    return redirect('notificações')

# ------------------- Projeto ----------------------


@login_required(login_url='login')
def convidaEquipe(request, projeto_id):
    ''' Pagina para convidar amigo para projeto'''
    user_profile = request.user.userprofile
    amigos = Relationship.objects.filter(sender_id=user_profile, status='aceito')
    convites = RelationshipEquipe.objects.filter(projeto_id=projeto_id)
    equipe = Equipe.objects.filter(projeto_id=projeto_id)
    if faz_parte_equipe(equipe, user_profile.id) == False:
        return redirect('home')
    amigos_convidados = []
    amigos_nao_convidados = []
    aceitos = []
    for membro in equipe:
        aceitos.append(membro.usuario)
    for convidado in convites:
        if convidado.status == "enviado":
            amigos_convidados.append(convidado.convidado)
    for amigo in amigos:
        if amigo.receiver not in amigos_convidados and amigo.receiver not in aceitos:
            amigos_nao_convidados.append(amigo)
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    return render(request, "tasks/equipe.html", {
        'equipe':equipe,
        'amigos_convidados': amigos_convidados,
        'amigos_nao_convidados': amigos_nao_convidados,
        'convites': convites,
        'projeto_id': projeto_id,
        'notificacao':notificacao
    })

@login_required(login_url='login')
def removerEquipe(request, amigo_id, projeto_id ):
    ''' Remover usuario da Equipe '''
    user_profile = request.user.userprofile
    amigo = get_object_or_404(UserProfile, id=amigo_id)
    RelationshipEquipe.objects.filter(usuario=user_profile, projeto_id=projeto_id, convidado=amigo).delete()
    Equipe.objects.filter(projeto_id=projeto_id, usuario=amigo).delete()
    RelationshipTarefa.objects.filter(usuario=amigo, tarefa__projeto_id=projeto_id ).delete()
    return redirect('convidaEquipe', projeto_id=projeto_id)

@login_required(login_url='login')
def cancelarConvite(request, convite_id, projeto_id):
    ''' Cancelar Convite enviado para o Projeto'''
    user_profile = request.user.userprofile
    convite = get_object_or_404(RelationshipEquipe, id=convite_id, projeto_id=projeto_id    )
    convite.delete()
    return redirect('convidaEquipe', projeto_id=convite.projeto_id)

@login_required(login_url='login')
def convidarAmigo(request, amigo_id,projeto_id):
    ''' Convidar Amigo para Projeto'''
    user_profile = request.user.userprofile
    amigo = get_object_or_404(UserProfile, id=amigo_id)

    if RelationshipEquipe.objects.filter(usuario=user_profile, projeto_id=projeto_id, convidado=amigo, status='enviado').exists():
        return redirect('convidaEquipe', projeto_id=projeto_id)
    else:
        convite = RelationshipEquipe(usuario=user_profile, projeto_id=projeto_id, convidado=amigo, status='enviado')
        convite.save()

    return redirect('convidaEquipe', projeto_id=projeto_id)

# ------------------- Tarefa ----------------------

def MembrosTarefa(request, projeto_id, tarefa_id):
        '''Pagina de Membros em Tarefas'''
        user_profile = request.user.userprofile
        equipes = Equipe.objects.filter(projeto=projeto_id)
        if faz_parte_equipe(equipes, user_profile.id) == False:
            return redirect('home')
        usuarioTarefa = RelationshipTarefa.objects.filter(tarefa__id= tarefa_id)
        notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
        notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
        notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
        equipeTarefa = [] 
        equipeSemTarefa = []
        for membro in usuarioTarefa:
            equipeTarefa.append(membro.usuario)
        for usuario in equipes:
            if not usuario.usuario in equipeTarefa:
                equipeSemTarefa.append(usuario.usuario)

        return render(request, 'tasks/membroTarefa.html',{'equipe':equipeSemTarefa,'usuarios':equipeTarefa, 'projeto_id':projeto_id, 'tarefa':tarefa_id, 'notificacao':notificacao})

def addMembroTarefa(request, projeto_id, usuario_id, tarefa_id):
    '''Adicionar membro a Tarefas'''
    usuario = get_object_or_404(UserProfile, id=usuario_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    convite = RelationshipTarefa(usuario=usuario, tarefa=tarefa)
    convite.save()
    return redirect('MembrosTarefa', projeto_id=projeto_id, tarefa_id=tarefa_id)

def popMembroTarefa(request, projeto_id, usuario_id, tarefa_id):
    '''Remover membro da Tarefa'''
    usuario = get_object_or_404(UserProfile, id=usuario_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    RelationshipTarefa.objects.filter(usuario=usuario, tarefa=tarefa).delete()
    return redirect('MembrosTarefa', projeto_id=projeto_id, tarefa_id=tarefa_id)


# ------------------- Editar Projeto ----------------------

def editar_projeto(request, projeto_id):
    user_profile = request.user.userprofile
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    if not request.user.is_authenticated:
        return redirect('login')
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            projeto = form.save(commit=False)  
            projeto.usuario = request.user
            projeto.save() 
            messages.success(request,"Projeto Editado!")
            return redirect('projeto', projeto_id)
    else:
        form = ProjetoForm(instance=projeto)
    return render(request, 'tasks/projetoCreate.html', {'form': form, 'projeto_id': projeto_id,  'projetos': todosProjetos, 'notificacao':notificacao})

@login_required(login_url='login')
def excluirProjeto(request, projeto_id ):
    Projeto.objects.filter(id=projeto_id).delete()
    messages.success(request,"Projeto Excluido!")
    return redirect('home')

# ------------------- Editar Tarefa ----------------------


def editar_tarefa(request, tarefa_id, projeto_id):
    user_profile = request.user.userprofile
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    if not request.user.is_authenticated:
        return redirect('login')
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            tarefa = form.save(commit=False)  
            tarefa.usuario = request.user
            tarefa.save() 
            messages.success(request,"Tarefa Editada!")
            return redirect('projeto', projeto_id)
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'tasks/tarefaCreate.html', {'form': form, 'tarefa_id': tarefa_id, 'projeto_id': projeto_id,  'projetos': todosProjetos, 'notificacao':notificacao})


@login_required(login_url='login')
def excluirTarefa(request, tarefa_id, projeto_id ):
    Tarefa.objects.filter(id=tarefa_id).delete()
    messages.success(request,"Tarefa Excluida!")
    return redirect('projeto', projeto_id)





def faz_parte_equipe(equipe, user_id):
    '''Verica se o usuario faz parte da equipe'''
    time = []
    for membro in equipe:
        time.append(membro.usuario.id)
    if user_id not in time:
        return False
    else:
        return True
