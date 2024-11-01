# Generated by Django 5.1 on 2024-10-31 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('usuario_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('genero', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=10, null=True)),
                ('altura', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('peso', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('obra_social', models.TextField(blank=True, null=True)),
                ('email_verificado', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('puntaje_sueno', models.DecimalField(decimal_places=2, max_digits=5)),
                ('observacion', models.TextField()),
                ('apnea_porcentaje', models.IntegerField(blank=True, null=True)),
                ('resultado_apnea', models.CharField(blank=True, max_length=255, null=True)),
                ('promedio_oxigeno', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('evaluacion_oxigeno', models.CharField(blank=True, max_length=255, null=True)),
                ('promedio_heart_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('evaluacion_heart_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('promedio_breathing', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('evaluacion_breathing', models.CharField(blank=True, max_length=255, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SomnoAIApp.usuarios')),
            ],
            options={
                'verbose_name': 'Observación',
                'verbose_name_plural': 'Observaciones',
            },
        ),
        migrations.CreateModel(
            name='Informes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('contenido_informe', models.TextField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SomnoAIApp.usuarios')),
            ],
            options={
                'verbose_name': 'Informe',
                'verbose_name_plural': 'Informes',
            },
        ),
        migrations.CreateModel(
            name='Estadisticas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('frecuencia_cardiaca', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('saturacion_oxigeno', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('movimientos', models.IntegerField(blank=True, null=True)),
                ('ronquidos', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('respiracion', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('presion_arterial', models.CharField(blank=True, max_length=15, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SomnoAIApp.usuarios')),
            ],
            options={
                'verbose_name': 'Estadística',
                'verbose_name_plural': 'Estadísticas',
            },
        ),
    ]
