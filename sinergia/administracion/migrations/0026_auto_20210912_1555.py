# Generated by Django 3.2.3 on 2021-09-12 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0025_citas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagosproveedores',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.proveedor', verbose_name='Cliente'),
        ),
        migrations.CreateModel(
            name='DeudaProveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha del pago')),
                ('estado_pagado', models.BooleanField(default=False, verbose_name='Estado de la deuda')),
                ('prestamo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administracion.prestamos', verbose_name='Prestamo')),
            ],
            options={
                'verbose_name': 'Deuda con proveedores',
                'verbose_name_plural': 'Deudas con proveedores',
            },
        ),
        migrations.AddField(
            model_name='pagosproveedores',
            name='deuda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administracion.deudaproveedor', verbose_name='Deuda'),
        ),
    ]
