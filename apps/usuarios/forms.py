from django import forms
from usuarios.models import *

class LoginForms(forms.Form):
    nome_login = forms.CharField(
        label="Login",
        required= True,
        max_length= 100,
        widget= forms.TextInput(
            attrs={
                "placeholder":'Usuario:'
            }
        )
    )
    senha = forms.CharField(
        label='Senha',
        required=True,
        max_length=30,
        widget= forms.PasswordInput(
            attrs={
                "placeholder":'Senha:'
            }
        )
    )

class CadastroForms(forms.Form):
    nome_cadastro=forms.CharField(
        label='Login', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'input-login',
                'placeholder': 'Usuário',
            }
        )
    )
    email=forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'input-login',
                'placeholder': 'Email',
            }
        )
    )
    senha_1=forms.CharField(
        label='Senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-login',
                'placeholder': 'Senha',
            }
        ),
    )
    senha_2=forms.CharField(
        label='Senha2', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-login',
                'placeholder': 'Senha novamente',
            }
        ),
    )
   
    def clean_nome_cadastro(self):
        nome = self.cleaned_data.get('nome_cadastro')

        if nome:
            nome = nome.strip()
            if ' ' in nome:
                raise forms.ValidationError('Espaços não são permitidos nesse campo')
            else:
                return nome

    def clean_senha_2(self):
        senha_1 = self.cleaned_data.get('senha_1')
        senha_2 = self.cleaned_data.get('senha_2')

        if senha_1 and senha_2:
            if senha_1 != senha_2:
                raise forms.ValidationError('Senhas não são iguais')
            else:
                return senha_2
            




from django import forms
from .models import UserProfile

class UserProfileForms(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nome', 'sobrenome', 'empresa', 'avatar']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'input-login',
                'placeholder': 'Nome',
            }),
            'sobrenome': forms.TextInput(attrs={
                'class': 'input-login',
                'placeholder': 'Sobrenome',
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'input-login',
                'placeholder': 'Empresa',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'input-login',  # Ajuste as classes conforme necessário
            }),
        }
