# Generated by Django 3.2.3 on 2021-06-14 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0008_clientes_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='otros_datos',
            field=models.TextField(blank=True, null=True, verbose_name='Otros datos'),
        ),
    ]
