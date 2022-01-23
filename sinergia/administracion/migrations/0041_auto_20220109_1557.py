# Generated by Django 3.2.3 on 2022-01-09 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0040_auto_20220109_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='code_key',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='password',
        ),
        migrations.AddField(
            model_name='clientes',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='administracion.userprofile', verbose_name='Usuario del sistema'),
        ),
    ]
