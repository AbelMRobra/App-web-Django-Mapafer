# Generated by Django 3.2.3 on 2021-07-25 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0020_alter_clientes_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuotasPrestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha del pago')),
                ('monto', models.FloatField(verbose_name='Monto')),
                ('estado', models.CharField(blank=True, choices=[('NO', 'No'), ('SI', 'Si'), ('PARCIAL', 'Parcial')], max_length=20, null=True, verbose_name='Estado')),
                ('prestamo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.prestamos', verbose_name='Prestamo asociado')),
            ],
            options={
                'verbose_name': 'Cuota',
                'verbose_name_plural': 'Cuotas',
            },
        ),
    ]
