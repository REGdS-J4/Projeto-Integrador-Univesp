# Generated by Django 5.0.4 on 2024-05-07 22:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0016_mensagem_salabatepapo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salabatepapo',
            name='mensagens',
        ),
        migrations.RemoveField(
            model_name='salabatepapo',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='aluno',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='professor',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Mensagem',
        ),
        migrations.DeleteModel(
            name='SalaBatePapo',
        ),
    ]
