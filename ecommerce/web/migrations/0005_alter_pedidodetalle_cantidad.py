# Generated by Django 3.2 on 2023-12-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20231207_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodetalle',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]