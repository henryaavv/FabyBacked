# Generated by Django 3.2 on 2023-12-07 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_pedidodetalle_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='direccion_envio',
            field=models.TextField(null=True),
        ),
    ]