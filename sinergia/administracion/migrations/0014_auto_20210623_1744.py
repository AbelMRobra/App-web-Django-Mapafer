# Generated by Django 3.2.3 on 2021-06-23 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0013_clientes_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='code_key',
            field=models.IntegerField(blank=True, null=True, verbose_name='Code key'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='password',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='password'),
        ),
    ]
