from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

#view que verifica se o usuario pertence ao grupo que esta logando.
def usuario_e_deste_grupo(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return user.groups.filter(name=group_name).exists()
    except Group.DoesNotExist:
        return False

#views para filtrar quem acessa cada pagina.
def escola(user):
    return user.groups.filter(name='Escola').exists()

def professor(user):
    return user.groups.filter(name='Professor').exists()

def aluno(user):
    return user.groups.filter(name='Aluno').exists()

#view para pagina de bloqueio.
def pagina_bloqueada(request):
    return render(request, 'bloqueada.html')

#VIEWS DA PARTE TODA DE LOGIN.
################################################################################################
#View para logar.
def tipo_de_login(request):
    return render(request, 'login/tipo_de_login.html')

#View para logar como "adm" da escola.
def login_da_escola(request):
    if request.method != 'POST':
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login/login_da_escola.html', context)
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = request.POST.get('usuario')
            senha = request.POST.get('senha')
            logar = authenticate(username=usuario, password=senha)
        
            if logar:
                login(request, logar)
                return redirect(reverse('indexescola'))
            else:
                messages.error(request,'Usuário ou Senha inválido.')
                return redirect(reverse('log_esc'))
#View para logar como professor.
def login_do_professor(request):
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = request.POST.get('usuario')
            senha = request.POST.get('senha')
            logar = authenticate(username=usuario, password=senha)
        
            if logar:
                login(request, logar)
                if usuario_e_deste_grupo(request.user, 'Professor'):
                    professor = Professor.objects.get(usuario=request.user)
                    return redirect(reverse('ind_pro', args=[professor.id]))
                else:
                    return redirect(reverse('block'))
            else:
                messages.error(request, 'Usuário ou Senha inválido.')
                return redirect(reverse('log_pro'))
    context = {'form': form}
    return render(request, 'login/login_do_professor.html', context)

#View para logar como aluno.
def login_do_aluno(request):
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = request.POST.get('usuario')
            senha = request.POST.get('senha')
            logar = authenticate(username=usuario, password=senha)
        
            if logar:
                login(request, logar)
                if usuario_e_deste_grupo(request.user, 'Aluno'):
                    aluno = Aluno.objects.get(usuario=request.user)
                    return redirect(reverse('ind_alu', args=[aluno.id]))
                else:
                    return redirect(reverse('block'))
            else:
                messages.error(request, 'Usuário ou Senha inválido.')
                return redirect(reverse('log_alu'))
    context = {'form': form}
    return render(request, 'login/login_do_aluno.html', context)

#View para deslogar
def deslogar(request):
    logout(request)
    return render(request, 'login/deslogar.html')

#View para registrar um novo login.
@user_passes_test(escola)
def registrar_novo_login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        grupo_login = request.POST.get('grupo_login')
        novo_usuario = User.objects.create_user(username=usuario, password=senha, first_name=primeiro_nome, last_name=ultimo_nome)
        novo_usuario.groups.add(grupo_login)
        novo_usuario.save()
        return redirect(reverse('indexescola'))
    return render(request, 'login/registrar_novo_login.html')

################################################################################################

#VIEWS DA PARTE TODA DE PAGINAS EXCLUSIVAS.
################################################################################################
#View da pagina de gerenciamento.
@user_passes_test(escola)
def index_escola(request):
    return render(request, 'gerenciamento/index.html')

#Views da parte dos professores no gerenciamento.
@user_passes_test(escola)
def listar_professores(request):
    professores = Professor.objects.all()
    context = {'professores': professores}
    return render(request, 'gerenciamento/professor/professores.html', context)

@user_passes_test(escola)
def informacoes_do_professor(request, id):
    professor = Professor.objects.get(id=id)
    context = {'professor': professor}
    return render(request, 'gerenciamento/professor/professor.html', context)

@user_passes_test(escola)
def registrar_novo_professor(request):
    if request.method != 'POST':
        form = ProfessorForm()
    else:
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('lis_pros'))
    context = {'form': form}
    return render(request, 'gerenciamento/professor/registrar_novo_professor.html', context)

@user_passes_test(escola)
def editar_informacoes_do_professor(request, id):
    professor = Professor.objects.get(id=id)
    if request.method != 'POST':
        form = ProfessorForm(instance=professor)
    else:
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect(reverse('inf_pro', args=[professor.id]))
    context = {'professor': professor, 'form': form}
    return render(request, 'gerenciamento/professor/editar_informacoes_do_professor.html', context)

@user_passes_test(escola)
def deletar_registro_do_professor(request, id):
    professor = get_object_or_404(Professor, id=id)

    if request.method == 'POST':
        # Se o formulário de confirmação for enviado, exclua o professor
        professor.delete()
        return redirect(reverse('lis_pros')) # Redireciona para a lista de professores

    # Caso contrário, exiba a página de confirmação
    context = {'professor': professor}
    return render(request, 'gerenciamento/professor/deletar_registro_do_professor.html', context)

#Views da parte dos alunos no gerenciamento.
@user_passes_test(escola)
def listar_alunos(request):
    alunos = Aluno.objects.all()
    context = {'alunos': alunos}
    return render(request, 'gerenciamento/aluno/alunos.html', context)

@user_passes_test(escola)
def informacoes_do_aluno(request, id):
    aluno = Aluno.objects.get(id=id)
    context = {'aluno': aluno}
    return render(request, 'gerenciamento/aluno/aluno.html', context)

@user_passes_test(escola)
def registrar_novo_aluno(request):
    if request.method != 'POST':
        form = AlunoForm()
    else:
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('lis_alus'))
    context = {'form': form}
    return render(request, 'gerenciamento/aluno/registrar_novo_aluno.html', context)

@user_passes_test(escola)
def editar_informacoes_do_aluno(request, id):
    aluno = Aluno.objects.get(id=id)
    if request.method != 'POST':
        form = AlunoForm(instance=aluno)
    else:
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect(reverse('inf_alu', args=[aluno.id]))
    context = {'aluno': aluno, 'form': form}
    return render(request, 'gerenciamento/aluno/editar_informacoes_do_aluno.html', context)

@user_passes_test(escola)
def deletar_registro_do_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        aluno.delete()
        return redirect(reverse('lis_alus'))
    context = {'aluno': aluno}
    return render(request, 'gerenciamento/aluno/deletar_registro_do_aluno.html', context)

#Views da parte dos cursos no gerenciamento.
@user_passes_test(escola)
def listar_cursos(request):
    cursos = Curso.objects.all()
    context = {'cursos': cursos}
    return render(request, 'gerenciamento/curso/cursos.html', context)

@user_passes_test(escola)
def informacoes_do_curso(request, id):
    curso = Curso.objects.get(id=id)
    context = {'curso': curso}
    return render(request, 'gerenciamento/curso/curso.html', context)

@user_passes_test(escola)
def registrar_novo_curso(request):
    if request.method != 'POST':
        form = CursoForm()
    else:
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('lis_curs'))
    context = {'form': form}
    return render(request, 'gerenciamento/curso/registrar_novo_curso.html', context)

@user_passes_test(escola)
def editar_informacoes_do_curso(request, id):
    curso = Curso.objects.get(id=id)
    if request.method != 'POST':
        form = CursoForm(instance=curso)
    else:
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect(reverse('inf_cur', args=[curso.id]))
    context = {'curso': curso, 'form': form}
    return render(request, 'gerenciamento/curso/editar_informacoes_do_curso.html', context)

@user_passes_test(escola)
def deletar_registro_do_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        curso.delete()
        return redirect(reverse('lis_curs'))
    context = {'curso': curso}
    return render(request, 'gerenciamento/curso/deletar_registro_do_curso.html', context)

#Views da parte das turmas no gerenciamento.
@user_passes_test(escola)
def listar_turmas(request):
    turmas = Turma.objects.all()
    context = {'turmas': turmas}
    return render(request, 'gerenciamento/turma/turmas.html', context)

@user_passes_test(escola)
def informacoes_da_turma(request, id):
    turma = Turma.objects.get(id=id)
    context = {'turma': turma}
    return render(request, 'gerenciamento/turma/turma.html', context)

@user_passes_test(escola)
def registrar_nova_turma(request):
    if request.method != 'POST':
        form = TurmaForm()
    else:
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('lis_turs'))
    context = {'form': form}
    return render(request, 'gerenciamento/turma/registrar_nova_turma.html', context)

@user_passes_test(escola)
def editar_informacoes_da_turma(request, id):
    turma = Turma.objects.get(id=id)
    if request.method != 'POST':
        form = TurmaForm(instance=turma)
    else:
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect(reverse('inf_tur', args=[turma.id]))
    context = {'turma': turma, 'form': form}
    return render(request, 'gerenciamento/turma/editar_informacoes_da_turma.html', context)

@user_passes_test(escola)
def deletar_registro_da_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        turma.delete()
        return redirect(reverse('lis_turs'))
    context = {'turma': turma}
    return render(request, 'gerenciamento/turma/deletar_registro_da_turma.html', context)

#Views da parte das aulas no gerenciamento.
@user_passes_test(escola)
def listar_aulas(request):
    aulas = Aula.objects.all().order_by('-id')
    turmas = Turma.objects.all()
    professor = Professor.objects.all()
    context = {'aulas': aulas, 'turmas':turmas, 'professor':professor}
    return render(request, 'gerenciamento/aula/aulas.html', context)

@user_passes_test(escola)
def filtrar_aulas(request):
    if 'turma' in request.GET:
        turma = request.GET['turma']
        aulas = Aula.objects.filter(turma_id=turma)
    elif 'professor' in request.GET:
        professor = request.GET['professor']
        aulas = Aula.objects.filter(professor_id=professor)
    else:
        aulas = Aula.objects.all()

    context = {'aulas': aulas, 'aulas':aulas}
    return render(request, 'gerenciamento/aula/filtrar_aulas.html', context)

@user_passes_test(escola)
def registrar_nova_aula(request):
    if request.method != 'POST':
        form = AulaForm()
    else:
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('lis_auls'))
    context = {'form': form}
    return render(request, 'gerenciamento/aula/registrar_nova_aula.html', context)

@user_passes_test(escola)
def editar_informacoes_da_aula(request, id):
    aula = Aula.objects.get(id=id)
    if request.method != 'POST':
        form = AulaForm(instance=aula)
    else:
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            return redirect(reverse('lis_auls'))
    context = {'aula': aula, 'form': form}
    return render(request, 'gerenciamento/aula/editar_informacoes_da_aula.html', context)

@user_passes_test(escola)
def deletar_registro_da_aula(request, id):
    aula = get_object_or_404(Aula, id=id)
    if request.method == 'POST':
        aula.delete()
        return redirect(reverse('lis_auls'))
    context = {'aula': aula}
    return render(request, 'gerenciamento/aula/deletar_registro_da_aula.html', context)

#Views da parte das mensagens no gerenciamento.

@user_passes_test(escola)
def mensagens(request):
    mensagens_enviadas = Mensagem.objects.filter(remetente=request.user).order_by("-data_hora")
    mensagens_recebidas = Mensagem.objects.filter(destinatario=request.user).order_by("-data_hora")

    context = {"m_e":mensagens_enviadas, "m_r":mensagens_recebidas}
    return render(request, 'gerenciamento/mensagem/mensagens.html', context)

@user_passes_test(escola)
def mensagem(request, id):
    mensagem = get_object_or_404(Mensagem, id=id)
    if request.user == mensagem.destinatario or request.user == mensagem.remetente:
        if request.method != "POST":
            form = RespostaForm()
        else:
            form = RespostaForm(request.POST)
            if form.is_valid():
                resposta = form.cleaned_data["conteudo"]
                nova_mensagem = Mensagem.objects.create(remetente=request.user, destinatario=mensagem.remetente, assunto=mensagem.assunto, conteudo=resposta)
                return redirect(reverse("msg", args=[nova_mensagem.id]))
        context = {
            'mensagem': mensagem, 'form': form
            }
        return render(request, 'gerenciamento/mensagem/mensagem.html', context)
    else:
        return redirect(reverse('block'))

@user_passes_test(escola)
def enviar_nova_mensagem(request):
    if request.method != 'POST':
        form = MensagemForm()
    else:
        form = MensagemForm(request.POST)
        if form.is_valid():
            nova_mensagem = form.save(commit=False)
            if nova_mensagem.destinatario != request.user:
                nova_mensagem.remetente = request.user
                form.save()
                return redirect(reverse('msgs'))
            else:
                messages.error(request, "Você não pode enviar uma mensagem a si mesmo.")
                return redirect(reverse('env_msg'))
    context = {'form': form}
    return render(request, 'gerenciamento/mensagem/enviar_nova_mensagem.html', context)

@user_passes_test(escola)
def deletar_mensagem(request, id):
    mensagem = get_object_or_404(Mensagem, id=id)
    if request.method == 'POST':
        mensagem.delete()
        return redirect(reverse('msgs'))
    context = {'mensagem': mensagem}
    return render(request, 'gerenciamento/mensagem/deletar_mensagem.html', context)

@user_passes_test(escola)
def editar_mensagem(request, id):
    mensagem = get_object_or_404(Mensagem, id=id)
    if request.method != 'POST':
        form = MensagemForm(instance=mensagem)
    else:
        form = MensagemForm(request.POST, instance=mensagem)
        if form.is_valid():
            form.save()
            return redirect(reverse('msg', args=[mensagem.id]))
    context = {'mensagem': mensagem, 'form': form}
    return render(request, 'gerenciamento/mensagem/editar_mensagem.html', context)

#Views exclusivas do login do professor.
@user_passes_test(professor)
def index_professor(request, id):
    professor = Professor.objects.get(id=id)
    turmas = Turma.objects.filter(professor=professor)
    context = {'professor':professor, 'turmas':turmas}
    return render(request, 'professor/index_professor.html', context)

@user_passes_test(professor)
def index_professor_agenda(request, id):
    professor = Professor.objects.get(id=id)
    turmas = Turma.objects.all()
    dias = DiaDaSemana.objects.all()
    horas = HoraDoDia.objects.all().order_by('hora')
    aulas = Aula.objects.filter(professor=professor)
    aulas_por_hora_semana = {}
    for hora in horas:
        aulas_por_semana = {}
        for dia in dias:
            aula = aulas.filter(hora_do_dia=hora, dia_da_semana=dia).first()
            aulas_por_semana[dia] = aula
        aulas_por_hora_semana[hora] = aulas_por_semana
    context = {
        'professor':professor,
        'aulas':aulas,
        'dias':dias,
        'horas':horas,
        'aulas_por_hora_semana':aulas_por_hora_semana,
        'turmas':turmas,
    }
    return render(request, 'professor/index_professor_agenda.html', context)

@user_passes_test(professor)
def index_professor_mensagens(request, id):
    professor = Professor.objects.get(id=id)
    mensagens_enviadas = Mensagem.objects.filter(remetente=request.user).order_by("-data_hora")
    mensagens_recebidas = Mensagem.objects.filter(destinatario=request.user).order_by("-data_hora")
    context = {"professor":professor, "m_e":mensagens_enviadas, "m_r":mensagens_recebidas}
    return render(request, 'professor/index_professor_mensagens.html', context)

@user_passes_test(professor)
def index_professor_mensagem(request, id, pk):
    professor = Professor.objects.get(id=id)
    mensagem = get_object_or_404(Mensagem, id=pk)
    if request.user == mensagem.destinatario or request.user == mensagem.remetente:
        if request.method != "POST":
            form = RespostaForm()
        else:
            form = RespostaForm(request.POST)
            if form.is_valid():
                resposta = form.cleaned_data["conteudo"]
                nova_mensagem = Mensagem.objects.create(remetente=request.user, destinatario=mensagem.remetente, assunto=mensagem.assunto, conteudo=resposta)
                return redirect(reverse("ind_pro_msg", args=[professor.id, nova_mensagem.id]))
        context = {
            'professor':professor, 'mensagem': mensagem, 'form': form
            }
        return render(request, 'professor/index_professor_mensagem.html', context)
    else:
        return redirect(reverse('block'))

@user_passes_test(professor)    
def index_professor_enviar_nova_mensagem(request, id):
    professor = Professor.objects.get(id=id)
    if request.method != 'POST':
        form = MensagemForm()
    else:
        form = MensagemForm(request.POST)
        if form.is_valid():
            nova_mensagem = form.save(commit=False)
            if nova_mensagem.destinatario != request.user:
                nova_mensagem.remetente = request.user
                form.save()
                return redirect(reverse('ind_pro_msgs', args=[professor.id]))
            else:
                messages.error(request, "Você não pode enviar uma mensagem a si mesmo.")
                return redirect(reverse('ind_pro_env_msg', args=[professor.id]))
    context = {'professor':professor, 'form': form}
    return render(request, 'professor/index_professor_enviar_nova_mensagem.html', context)

#Views exclusivas do login do aluno.
@user_passes_test(aluno)
def index_aluno(request, id):
    aluno = Aluno.objects.get(id=id)
    context = {'aluno':aluno}
    return render(request, 'aluno/index_aluno.html', context)

@user_passes_test(aluno)
def index_aluno_agenda(request, id):
    aluno = Aluno.objects.get(id=id)
    turma = Turma.objects.all()
    turmas = Turma.objects.filter(aluno=aluno)
    dias = DiaDaSemana.objects.all()
    horas = HoraDoDia.objects.all().order_by('hora')
    aulas_por_hora_semana = {}
    for turma in turmas:
        aulas = Aula.objects.filter(turma=turma)
    for hora in horas:
        aulas_por_semana = {}
        for dia in dias:
            aula = aulas.filter(hora_do_dia=hora, dia_da_semana=dia).first()
            aulas_por_semana[dia] = aula
        aulas_por_hora_semana[hora] = aulas_por_semana    
    context = {'aluno':aluno,
               'turmas':turmas,
               'dias':dias,
               'horas':horas,
               'aulas':aulas,
               'aulas_por_hora_semana':aulas_por_hora_semana,
            }
    return render(request, 'aluno/index_aluno_agenda.html', context)

@user_passes_test(aluno)
def index_aluno_mensagens(request, id):
    aluno = Aluno.objects.get(id=id)
    mensagens_enviadas = Mensagem.objects.filter(remetente=request.user).order_by("-data_hora")
    mensagens_recebidas = Mensagem.objects.filter(destinatario=request.user).order_by("-data_hora")
    context = {'aluno':aluno, 'm_e':mensagens_enviadas, 'm_r':mensagens_recebidas}
    return render(request, 'aluno/index_aluno_mensagens.html', context)

@user_passes_test(aluno)
def index_aluno_mensagem(request, id, pk):
    aluno = Aluno.objects.get(id=id)
    mensagem = get_object_or_404(Mensagem, id=pk)
    if request.user == mensagem.destinatario or request.user == mensagem.remetente:
        if request.method != "POST":
            form = RespostaForm()
        else:
            form = RespostaForm(request.POST)
            if form.is_valid():
                resposta = form.cleaned_data["conteudo"]
                nova_mensagem = Mensagem.objects.create(remetente=request.user, destinatario=mensagem.remetente, assunto=mensagem.assunto, conteudo=resposta)
                return redirect(reverse("ind_alu_msg", args=[aluno.id, nova_mensagem.id]))
        context = {
            'aluno':aluno, 'mensagem': mensagem, 'form': form
            }
        return render(request, 'aluno/index_aluno_mensagem.html', context)
    else:
        return redirect(reverse('block'))
    
@user_passes_test(aluno)
def index_aluno_enviar_nova_mensagem(request, id):
    aluno = Aluno.objects.get(id=id)
    if request.method != 'POST':
        form = MensagemForm()
    else:
        form = MensagemForm(request.POST)
        if form.is_valid():
            nova_mensagem = form.save(commit=False)
            if nova_mensagem.destinatario != request.user:
                nova_mensagem.remetente = request.user
                form.save()
                return redirect(reverse('ind_alu_msgs', args=[aluno.id]))
            else:
                messages.error(request, "Você não pode enviar uma mensagem a si mesmo.")
                return redirect(reverse('ind_alu_env_msg', args=[aluno.id]))
    context = {'aluno':aluno, 'form': form}
    return render(request, 'aluno/index_aluno_enviar_nova_mensagem.html', context)