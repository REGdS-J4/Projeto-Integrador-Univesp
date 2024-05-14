from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.
class DiaDaSemana(models.Model):
    id = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=13, unique=True)

    class Meta:
        verbose_name_plural = 'Dias da Semana'
    def __str__(self):
        return self.dia
    
class HoraDoDia(models.Model):
    id = models.AutoField(primary_key=True)
    hora = models.TimeField(unique=True)

    class Meta:
        verbose_name_plural = 'Horas do Dia'
    def __str__(self):
        return self.hora.strftime('%H:%M')

class Pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=55)
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=9, unique=True)
    data_nascimento = models.DateField()
    email = models.EmailField(max_length=55, unique=True)
    telefone = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=55)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome
    
class Professor(Pessoa):
    carga_horaria_semanal = models.ManyToManyField(
        DiaDaSemana,
        through='CargaHorariaProfessor',
        related_name='carga_horaria_professores',
    )
    class Meta:
        verbose_name_plural = 'Professores'
    pass

#Quando adicionar um novo curso no banco de dados, coloque o nome do curso no arquivo "estilo.css" para estilizar na agenda do aluno.
class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=55)
    descricao = models.TextField(max_length=220)
    duracao = models.CharField(max_length=55)

    class Meta:
        verbose_name_plural = 'Cursos'
    def __str__(self):
        return self.nome

#Quando adicionar uma nova turma no banco de dados, coloque o nome da turma no arquivo "estilo.css" para estilizar na agenda do professor.
class Turma(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=55)
    professor = models.ManyToManyField(Professor, blank=True)
    carga_horaria_semanal = models.ManyToManyField(
        DiaDaSemana,
        through='CargaHorariaTurma',
        related_name='carga_horaria_turmas'
    )

    class Meta:
        verbose_name_plural = 'Turmas'

    def __str__(self):
        return self.nome
    
class CargaHorariaProfessor(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_da_semana = models.ForeignKey(DiaDaSemana, on_delete=models.CASCADE)
    horas_do_dia = models.ManyToManyField(HoraDoDia)

    class Meta:
        verbose_name_plural = 'Carga Horária dos Professores'

    def clean(self):
        if CargaHorariaProfessor.objects.filter(
            professor=self.professor,
            dia_da_semana=self.dia_da_semana
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Já existe uma carga horária para este professor neste dia.')
        
    def __str__(self):
        return f"{self.professor} - {self.dia_da_semana}"
    
class CargaHorariaTurma(models.Model):
    id = models.AutoField(primary_key=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    dia_da_semana = models.ForeignKey(DiaDaSemana, on_delete=models.CASCADE)
    horas_do_dia = models.ManyToManyField(HoraDoDia)

    class Meta:
        verbose_name_plural = 'Carga Horária das Turmas'

    def clean(self):
        if CargaHorariaTurma.objects.filter(
            turma=self.turma,
            dia_da_semana=self.dia_da_semana
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Já existe uma carga horária para esta turma neste dia.')
        
    def __str__(self):
        return f"{self.turma} - {self.dia_da_semana}"
    
class Aluno(Pessoa):
    curso = models.ManyToManyField(Curso, blank=True)
    turma = models.ForeignKey(Turma, blank=True, on_delete=models.CASCADE)
    data_matricula = models.DateField()
    situacao_matricula = models.BooleanField()

class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    dia_da_semana = models.ForeignKey(DiaDaSemana, on_delete=models.CASCADE)
    hora_do_dia = models.ForeignKey(HoraDoDia, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Aulas'

    def clean(self):
        if not CargaHorariaProfessor.objects.filter(
            professor=self.professor,
            dia_da_semana=self.dia_da_semana,
        ).exists():
            raise ValidationError(('Não há carga horária definida para o professor {} neste dia da semana.').format(self.professor))
        
        if not CargaHorariaTurma.objects.filter(
            turma=self.turma,
            dia_da_semana=self.dia_da_semana,
        ).exists():
            raise ValidationError(('Não há carga horária definida para a turma {} neste dia da semana.').format(self.turma))

        if Aula.objects.filter(
            dia_da_semana=self.dia_da_semana,
            hora_do_dia=self.hora_do_dia,
            professor=self.professor,
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Este professor já possui outra aula marcada neste horário.')
        
        if Aula.objects.filter(
            dia_da_semana=self.dia_da_semana,
            hora_do_dia=self.hora_do_dia,
            turma=self.turma,
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Esta turma já possui outra aula marcada neste horário.')

    def __str__(self):
        return f"{self.curso} - {self.dia_da_semana} ({self.hora_do_dia})"
    
class Mensagem(models.Model):
    id = models.AutoField(primary_key=True)
    remetente = models.ForeignKey(User,on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User,on_delete=models.CASCADE, related_name='mensagens_recebidas')
    assunto = models.CharField(max_length=55)
    conteudo = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Mensagens'

    def __str__(self):
        return f"{self.remetente.first_name}: {self.conteudo}"