# Generated by Django 5.0.4 on 2024-05-01 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0008_alter_aluno_cpf_alter_aluno_email_alter_aluno_rg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='turma',
            field=models.ManyToManyField(blank=True, to='gerenciamento.turma'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='curso',
            field=models.ManyToManyField(blank=True, to='gerenciamento.curso'),
        ),
    ]
