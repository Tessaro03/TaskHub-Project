from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile, Relationship
from tasks.models import RelationshipEquipe
from django.contrib.auth.decorators import login_required
from tasks.models import Projeto, RelationshipTarefa
from usuarios.forms import LoginForms, CadastroForms, UserProfileForms
from django.contrib import messages


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForms()
    if request.method == 'POST':
        form = LoginForms(request.POST)
        try:
            if form.is_valid():
                nome = form['nome_login'].value()
                senha = form['senha'].value()
            usuario = auth.authenticate(
                request,
                username=nome,
                password=senha
            )
        except:
            return redirect('login')
        if usuario is not None:
            auth.login(request, usuario)
            return redirect('home')
        else:
            messages.error(request,"Falha ao Logar!")
            return redirect('login')
    return render(request, 'usuarios/login.html', {'form': form})


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CadastroForms()
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        if form['senha_1'].value() != form['senha_2'].value():
            messages.error(request,'As Senhas deve ser igual!')
            return redirect('cadastro')
        login = form['nome_cadastro'].value()
        email = form['email'].value()
        senha = form['senha_2'].value()

        if User.objects.filter(username=login).exists(): 
            messages.error(request,'Usuario já Existe')
            return redirect('cadastro')

        usuario = User.objects.create_user(
            username=login,
            email=email,
            password=senha,
        )    

        logar = auth.authenticate(
            request,
            username=login,
            password=senha
        )
        auth.login(request, logar)
        messages.success(request,"Cadastro feito com Sucesso")
        return redirect('userProfile')
    return render(request, 'usuarios/cadastro.html', {'form': form})


def userProfile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_profile = request.user.userprofile
    form = UserProfileForms()
    if request.method == 'POST':
        form = UserProfileForms(request.POST, request.FILES, instance=user_profile)
        login = form['nome'].value()
        sobrenome = form['sobrenome'].value()
        empresa = form['empresa'].value()
        avatar = form['avatar'].value        
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print("Erros de validação:", form.errors)
    else:
        form = UserProfileForms(instance=user_profile)
    return render(request, 'usuarios/userProfile.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def perfil(request, amigo_id=None):
    '''Pagina de Perfil do Usuario mostrando Amigos, Projetos e Tarefas'''
    user_profile = request.user.userprofile
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    usuario = UserProfile.objects.get(user=amigo_id)
    amigos = Relationship.objects.filter(sender=usuario, status='aceito')
    tarefas = RelationshipTarefa.objects.filter(usuario=usuario)
    todosProjetos = Projeto.objects.filter(equipe__usuario=usuario)
    relacionamentos = Relationship.objects.filter(sender=user_profile) 
    frindes = []
    for relacionado in relacionamentos:
        frindes.append(relacionado.receiver)
    if usuario == user_profile:
        situacao = ''
    elif usuario in frindes:
        situacao = Relationship.objects.get(sender=user_profile, receiver=usuario)
    else:
        situacao = "nenhum"

    if amigos.count == 0:
        amigos = 'Sem amigos'
    return render(request,'usuarios/perfil.html', {'projetos':todosProjetos,'usuario':usuario, 'amigos':amigos, 'notificacao':notificacao, 'tarefas':tarefas, "situacao":situacao})


@login_required(login_url='login')
def removerAmigo(request, amigo_id):
    user_profile = request.user.userprofile
    amigo = get_object_or_404(UserProfile, id=amigo_id)
    Relationship.objects.filter(sender=user_profile, receiver=amigo).delete()
    Relationship.objects.filter(receiver=user_profile, sender=amigo).delete()
    current_url = request.META.get('HTTP_REFERER', '/')
    return redirect(current_url)

def adicionarAmigo(request, amigo_id):
    user_profile = request.user.userprofile
    amigo = get_object_or_404(UserProfile, id=amigo_id)
    current_url = request.META.get('HTTP_REFERER', '/')
    if  Relationship.objects.filter(sender=user_profile, receiver=amigo, status='enviado').exists() or Relationship.objects.filter(sender=amigo, receiver=user_profile, status='enviado').exists():
        return redirect(current_url)
    else:
        Relationship.objects.create(sender=user_profile, receiver=amigo, status='enviado')
        return redirect(current_url)



@login_required(login_url='login')
def buscaUsuarios(request):
    user_profile = request.user.userprofile
    notificacaoEquipe = RelationshipEquipe.objects.filter(convidado=user_profile,status='enviado')
    notificacaoAmigo = Relationship.objects.filter(receiver=user_profile, status='enviado')
    notificacao = len(notificacaoEquipe) + len(notificacaoAmigo)
    todosProjetos = Projeto.objects.filter(equipe__usuario=user_profile)
    if "usuario" in request.GET:
        nome = request.GET['usuario']
        nome = nome.capitalize()
        usuarios = UserProfile.objects.filter(nome__icontains=nome)
        amigos = Relationship.objects.filter(sender=user_profile ,receiver__nome__icontains=nome)
        listaEnviado = []
        listaAmigo = []
        listaUsuario = []
        for amigo in amigos:
            if amigo.receiver != user_profile:
                if amigo.status == "aceito":
                    listaAmigo.append(amigo.receiver)
                else:
                    listaEnviado.append(amigo.receiver)
        for usuario in usuarios:
            if not usuario in listaAmigo and usuario != user_profile and not usuario in listaEnviado:
                listaUsuario.append(usuario)
    return render(request,'usuarios/buscaAmigos.html', {'projetos':todosProjetos, 'usuarios':listaUsuario, 'amigos':listaAmigo , 'notificacao':notificacao})

