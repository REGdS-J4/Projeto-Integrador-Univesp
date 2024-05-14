from django import forms
from .models import *


class LoginForm(forms.Form):
    usuario = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Usuário',
                'id':'usuario',
            }
        )
    )
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Senha',
                'id':'senha',
            }
        )
    )

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'
        labels = {
            'usuario': 'Usuário',
            'rg':'RG',
            'cpf':'CPF',
            'data_nascimento':'Data de Nascimento',
            'endereco':'Endereço',
            'carga_horaria_semanal':'Carga Horária Semanal',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class':'form-control'}),
            'nome': forms.TextInput(attrs={'class':'form-control', 'pattern':'^[a-zA-Z0-9\s\]+$', 'placeholder':'Digite o nome do Professor'}),
            'cpf': forms.TextInput(attrs={'class':'form-control','pattern':'^[0-9]+$', 'placeholder':'Digite somente números'}),
            'rg': forms.TextInput(attrs={'class':'form-control','pattern':'^[0-9]+$', 'placeholder':'Digite somente números'}),
            'data_nascimento': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'nome@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'+5513999999999'}),
            'endereco': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rua ABC, 123'}),
            'carga_horaria_semanal': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = '__all__'
        labels = {
            'usuario': 'Usuário',
            'rg':'RG',
            'cpf':'CPF',
            'data_nascimento':'Data de Nascimento',
            'endereco':'Endereço',
            'curso':'Curso(s)',
            'turma':'Turma',
            'data_matricula':'Data da Matrícula',
            'situacao_matricula':'Situacao da Matrícula',           
        }
        widgets = {
            'usuario': forms.Select(attrs={'class':'form-control'}),
            'nome': forms.TextInput(attrs={'class':'form-control', 'pattern':'^[a-zA-Z0-9\s\]+$', 'placeholder':'Digite o nome do Aluno'}),
            'cpf': forms.TextInput(attrs={'class':'form-control','pattern':'^[0-9]+$', 'placeholder':'Digite somente números'}),
            'rg': forms.TextInput(attrs={'class':'form-control','pattern':'^[0-9]+$', 'placeholder':'Digite somente números'}),
            'data_nascimento': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'nome@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'+5513999999999'}),
            'endereco': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rua ABC, 123'}),
            'curso': forms.SelectMultiple(attrs={'class':'form-control'}),
            'turma': forms.Select(attrs={'class':'form-control'}),
            'data_matricula': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'situacao_matricula': forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}),
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        labels = {
            'nome':'Nome do Curso',
            'descricao':'Descrição do Curso',
            'duracao':'Duração do Curso',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control', 'pattern':'^[a-zA-Z0-9\s\]+$', 'placeholder':'Digite o nome do Curso'}),
            'descricao': forms.Textarea(attrs={'class':'form-control', 'pattern':'^[a-zA-Z0-9\s\]+$', 'placeholder':'Digite a descrição do Curso'}),
            'duracao': forms.TextInput(attrs={'class':'form-control','pattern':'^[a-zA-Z0-9\s\]+$', 'placeholder':'000 horas'}),
        }

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = '__all__'
        labels = {
            'nome':'Nome da Turma',
            'professor':'Professor(es)',
            'carga_horaria_semanal':'Carga Horária Semanal'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control', 'pattern':'^[a-zA-Z0-9\s\]+$', 'placeholder':'Digite o nome da Turma'}),
            'professor': forms.SelectMultiple(attrs={'class':'form-control'}),
            'carga_horaria_semanal': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = '__all__'
        labels = {

        }
        widgets = {
            'curso': forms.Select(attrs={'class':'form-control'}),
            'dia_da_semana': forms.Select(attrs={'class':'form-control'}),
            'hora_do_dia': forms.Select(attrs={'class':'form-control'}),
            'professor': forms.Select(attrs={'class':'form-control'}),
            'turma': forms.Select(attrs={'class':'form-control'}),
            
        }

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ["destinatario", "assunto", "conteudo"]
        labels = {
            "destinatario": "Destinatário",
            "assunto": "Assunto",
            "conteudo": "Mensagem",
        }
        widgets = {
            "destinatario": forms.Select(attrs={'class':'form-control'}),
            "assunto": forms.TextInput(attrs={'class':'form-control'}),
            "conteudo": forms.Textarea(attrs={'class':'form-control'}),
        }

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ["conteudo"]
        labels = {
            "conteudo":"Resposta",
        }
        widgets = {
            "conteudo": forms.Textarea(attrs={'class':'form-control border border-2'}),
        }