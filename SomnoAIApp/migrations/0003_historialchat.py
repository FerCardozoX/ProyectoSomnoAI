# Generated by Django 5.1 on 2024-09-29 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SomnoAIApp', '0002_rename_condiciones_medicas_usuario_obra_social_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.TextField()),
                ('respuesta', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SomnoAIApp.usuario')),
            ],
        ),
    ]