# Generated by Django 3.1.4 on 2021-01-10 07:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tabelas', '0007_conta_data_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='data_compra',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
