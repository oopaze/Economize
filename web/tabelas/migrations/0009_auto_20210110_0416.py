# Generated by Django 3.1.4 on 2021-01-10 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabelas', '0008_auto_20210110_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='data_compra',
            field=models.DateField(),
        ),
    ]