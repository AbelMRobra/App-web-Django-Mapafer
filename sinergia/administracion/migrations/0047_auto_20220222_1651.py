# Generated by Django 3.2.3 on 2022-02-22 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0046_auto_20220217_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='localidad',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Localidad'),
        ),
        migrations.AddField(
            model_name='clientes',
            name='provincia',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Provincia'),
        ),
    ]
