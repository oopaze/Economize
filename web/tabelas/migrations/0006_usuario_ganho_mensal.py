# Generated by Django 3.1.4 on 2021-01-10 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabelas', '0005_parcelamento_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='ganho_mensal',
            field=models.DecimalField(decimal_places=2, default=1200, max_digits=12),
            preserve_default=False,
        ),
    ]