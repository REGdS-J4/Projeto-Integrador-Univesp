from django.contrib import admin
from .models import *

# Register your models here.
class CargaHorariaProfessorAdmin(admin.ModelAdmin):
   list_display = ('professor','dia_da_semana','listar_horas')
   list_filter = ('professor','dia_da_semana')
   
   def listar_horas(self, obj):
      horas_ordenada = obj.horas_do_dia.all().order_by('hora')
      return ", ".join([str(hora) for hora in horas_ordenada])

class CargaHorariaTurmaAdmin(admin.ModelAdmin):
   list_display = ('turma','dia_da_semana','listar_horas')
   list_filter = ('turma','dia_da_semana')

   def listar_horas(self, obj):
      horas_ordenada = obj.horas_do_dia.all().order_by('hora')
      return ", ".join([str(hora) for hora in horas_ordenada])

class ProfessorAdmin(admin.ModelAdmin):
   list_display = ('nome','email','usuario')

class AlunoAdmin(admin.ModelAdmin):
   list_display = ('nome','email','usuario','turma',)
   list_filter = ('turma',)
   
class AulaAdmin(admin.ModelAdmin):
   list_display = ('curso', 'dia_da_semana', 'hora_do_dia', 'professor', 'turma')
   list_filter = ('curso', 'dia_da_semana', 'hora_do_dia', 'professor', 'turma')

admin.site.register(DiaDaSemana)
admin.site.register(HoraDoDia)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Curso)
admin.site.register(Turma)
admin.site.register(CargaHorariaProfessor, CargaHorariaProfessorAdmin)
admin.site.register(CargaHorariaTurma, CargaHorariaTurmaAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Aula, AulaAdmin)
admin.site.register(Mensagem)