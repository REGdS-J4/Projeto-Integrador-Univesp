# Generated by Django 5.0.4 on 2024-05-04 22:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0012_curso_descricao_curso_duracao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='turma',
        ),
        migrations.AddField(
            model_name='aluno',
            name='turma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gerenciamento.turma'),
        ),
    ]
