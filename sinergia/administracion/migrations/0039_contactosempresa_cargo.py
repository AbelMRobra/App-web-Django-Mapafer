# Generated by Django 3.2.3 on 2021-11-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0038_auto_20211129_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactosempresa',
            name='cargo',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Cargo que ocupa'),
        ),
    ]
