# Generated by Django 3.1.4 on 2021-01-02 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabelas', '0002_auto_20201231_1908'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contas',
            new_name='Conta',
        ),
        migrations.CreateModel(
            name='Parcelamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=15)),
                ('conta_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tabelas.conta')),
            ],
        ),
    ]
