# Generated by Django 3.2.3 on 2021-06-14 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0007_auto_20210614_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Email'),
        ),
    ]
