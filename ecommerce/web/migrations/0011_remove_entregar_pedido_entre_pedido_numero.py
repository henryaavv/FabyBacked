# Generated by Django 3.2 on 2023-12-08 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20231208_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entregar_pedido',
            name='entre_pedido_numero',
        ),
    ]
