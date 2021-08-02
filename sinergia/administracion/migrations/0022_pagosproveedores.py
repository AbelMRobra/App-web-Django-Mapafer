# Generated by Django 3.2.3 on 2021-08-02 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0021_cuotasprestamo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagosProveedores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha del pago')),
                ('monto', models.FloatField(verbose_name='Monto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.proveedor', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Pago a proveedor',
                'verbose_name_plural': 'Pagos a proveedores',
            },
        ),
    ]
