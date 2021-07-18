# Generated by Django 3.2.3 on 2021-07-18 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0018_auto_20210718_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='bath_sit',
            field=models.CharField(blank=True, choices=[('ADENTRO', 'Adentro'), ('AFUERA', 'Afuera')], max_length=100, null=True, verbose_name='Baño situación'),
        ),
        migrations.AddField(
            model_name='clientes',
            name='deuda',
            field=models.CharField(blank=True, choices=[('SI', 'Si'), ('NO', 'No')], max_length=20, null=True, verbose_name='Deuda entidad bancaria'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='bathrooms',
            field=models.IntegerField(blank=True, null=True, verbose_name='Dormitorios'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='cuartos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ambientes'),
        ),
    ]
