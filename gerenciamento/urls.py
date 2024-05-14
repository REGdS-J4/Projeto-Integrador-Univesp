from django.urls import path
from . import views


urlpatterns = [
    #Rota para pagina de bloqueio. 
    path('pagina_bloqueada/', views.pagina_bloqueada, name='block'),
    #Rota pra saber quem está logando.
    path('', views.tipo_de_login, name='qel'),
    #Rotas de cada tipo de login.
    path('login_escola/', views.login_da_escola, name='log_esc'),
    path('login_professor/', views.login_do_professor, name='log_pro'),
    path('login_aluno/', views.login_do_aluno, name='log_alu'),
    #Rota para deslogar.
    path('deslogar/', views.deslogar, name='desl'),
    #Rota para adicionar um login.
    path('registrar_novo_login/', views.registrar_novo_login, name='add_log'),
    
    #Rotas para as paginas exclusiva do login da escola.
    #Index
    path('gerenciamento/', views.index_escola, name='indexescola'),
    #Professores.
    path('gerenciamento/professores/', views.listar_professores, name='lis_pros'),
    path('gerenciamento/professor/<int:id>', views.informacoes_do_professor, name='inf_pro'),
    path('gerenciamento/registrar_novo_professor/', views.registrar_novo_professor, name='add_pro'),
    path('gerenciamento/editar_informacoes_do_professor/<int:id>', views.editar_informacoes_do_professor, name='edi_inf_pro'),
    path('gerenciamento/deletar_registro_do_professor/<int:id>', views.deletar_registro_do_professor, name='del_pro'),
    #Alunos.
    path('gerenciamento/alunos/', views.listar_alunos, name='lis_alus'),
    path('gerenciamento/aluno/<int:id>', views.informacoes_do_aluno, name='inf_alu'),
    path('gerenciamento/registrar_novo_aluno/', views.registrar_novo_aluno, name='add_alu'),
    path('gerenciamento/editar_informacoes_do_aluno/<int:id>', views.editar_informacoes_do_aluno, name='edi_inf_alu'),
    path('gerenciamento/deletar_registro_do_aluno/<int:id>', views.deletar_registro_do_aluno, name='del_alu'),
    #Cursos.
    path('gerenciamento/cursos/', views.listar_cursos, name='lis_curs'),
    path('gerenciamento/curso/<int:id>', views.informacoes_do_curso, name='inf_cur'),
    path('gerenciamento/registrar_novo_curso/', views.registrar_novo_curso, name='add_cur'),
    path('gerenciamento/editar_informacoes_do_curso/<int:id>', views.editar_informacoes_do_curso, name='edi_inf_cur'),
    path('gerenciamento/deletar_registro_do_curso/<int:id>', views.deletar_registro_do_curso, name='del_cur'),
    #Turmas.
    path('gerenciamento/turmas/', views.listar_turmas, name='lis_turs'),
    path('gerenciamento/turma/<int:id>', views.informacoes_da_turma, name='inf_tur'),
    path('gerenciamento/registrar_nova_turma/', views.registrar_nova_turma, name='add_tur'),
    path('gerenciamento/editar_informacoes_da_turma/<int:id>', views.editar_informacoes_da_turma, name='edi_inf_tur'),
    path('gerenciamento/deletar_registro_da_turma/<int:id>', views.deletar_registro_da_turma, name='del_tur'),
    #Aulas.
    path('gerenciamento/aulas/', views.listar_aulas, name='lis_auls'),
    path('gerenciamento/filtrar_aulas/', views.filtrar_aulas, name='fil_auls'),
    path('gerenciamento/registrar_nova_aula/', views.registrar_nova_aula, name='add_aul'),
    path('gerenciamento/editar_informacoes_da_aula/<int:id>', views.editar_informacoes_da_aula, name='edi_inf_aul'),
    path('gerenciamento/deletar_registro_da_aula/<int:id>', views.deletar_registro_da_aula, name='del_aul'),
    #Mensagens.
    path('gerenciamento/mensagens/', views.mensagens, name='msgs'),
    path('gerenciamento/mensagem/<int:id>', views.mensagem, name='msg'),
    path('gerenciamento/enviar_nova_mensagem/', views.enviar_nova_mensagem, name='env_msg'),

    #Rotas para as paginas exclusivas do login do professor.
    path('index_professor/<int:id>/', views.index_professor, name='ind_pro'),
    path('index_professor/<int:id>/agenda/', views.index_professor_agenda, name='ind_pro_age'),
    path('index_professor/<int:id>/mensagens/', views.index_professor_mensagens, name='ind_pro_msgs'),
    path('index_professor/<int:id>/mensagem/<int:pk>', views.index_professor_mensagem, name='ind_pro_msg'),
    path('index_professor/<int:id>/enviar_nova_mensagem/', views.index_professor_enviar_nova_mensagem, name='ind_pro_env_msg'),

    #Rotas para as paginas exclusivas do login do aluno.
    path('index_aluno/<int:id>/', views.index_aluno, name='ind_alu'),
    path('index_aluno/<int:id>/agenda/', views.index_aluno_agenda, name='ind_alu_age'),
    path('index_aluno/<int:id>mensagens/', views.index_aluno_mensagens, name='ind_alu_msgs'),
    path('index_aluno/<int:id>/mensagem/<int:pk>', views.index_aluno_mensagem, name='ind_alu_msg'),
    path('index_aluno/<int:id>/enviar_nova_mensagem/', views.index_aluno_enviar_nova_mensagem, name='ind_alu_env_msg'),


    #path('', views., name=''),
]