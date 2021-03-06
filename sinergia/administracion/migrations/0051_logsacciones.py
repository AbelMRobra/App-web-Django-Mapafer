# Generated by Django 3.2.3 on 2022-04-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0050_movimientocontable_cuenta'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogsAcciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('accion', models.CharField(max_length=200, verbose_name='Accion')),
                ('resultado', models.CharField(max_length=200, verbose_name='Accion')),
            ],
            options={
                'verbose_name': 'Log de acciones del sistema',
                'verbose_name_plural': 'Logs de acciones del sistema',
            },
        ),
    ]
