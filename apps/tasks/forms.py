from django import forms
from tasks.models import Projeto, Tarefa

class ProjetoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Projeto
        labels = {
            'descricao': 'Descrição',
            'data_inicio': 'Data Inicial',
            'data_termino': 'Data Final',
        }
        widgets = {
            'usuario': forms.HiddenInput(),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'cor': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'data_termino': forms.DateInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        exclude = ['usuario']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.usuario = self.user
        if commit:
            instance.save()
        return instance

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        exclude = ['']
        labels = {
            'descricao': 'Descrição',
            'data_inicio': 'Data Inicial',
            'data_termino': 'Data Final',
            'completa':'Completa',
            'projeto':'Projeto',
        }
        widgets = {
            'projeto': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'data_termino': forms.DateInput(attrs={'class': 'form-control'}),
            'completa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }