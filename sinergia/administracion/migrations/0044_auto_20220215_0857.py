# Generated by Django 3.2.3 on 2022-02-15 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0043_empresa_cuit'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='ciudad',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Ciudad'),
        ),
        migrations.AddField(
            model_name='clientes',
            name='provincia',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Provincia'),
        ),
    ]
