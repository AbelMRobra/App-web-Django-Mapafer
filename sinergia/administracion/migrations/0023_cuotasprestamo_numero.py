# Generated by Django 3.2.3 on 2021-08-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0022_pagosproveedores'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuotasprestamo',
            name='numero',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Numero'),
        ),
    ]
