# Generated by Django 3.2.4 on 2021-08-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210824_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nrvolcoeff',
            name='vol_c0',
            field=models.FloatField(help_text='coeficiente ordem 0: nr^0', verbose_name='Volume água c0'),
        ),
        migrations.AlterField(
            model_name='nrvolcoeff',
            name='vol_c1',
            field=models.FloatField(help_text='coeficiente ordem 1: nr^1', verbose_name='Volume água c1'),
        ),
        migrations.AlterField(
            model_name='nrvolcoeff',
            name='vol_c2',
            field=models.FloatField(help_text='coeficiente ordem 2: nr^2', verbose_name='Volume água c2'),
        ),
        migrations.AlterField(
            model_name='nrxcgcoeff',
            name='xcg_c0',
            field=models.FloatField(help_text='coeficiente ordem 0: nr^0', verbose_name='Xcg água c0'),
        ),
        migrations.AlterField(
            model_name='nrxcgcoeff',
            name='xcg_c1',
            field=models.FloatField(help_text='coeficiente ordem 1: nr^1', verbose_name='Xcg água c1'),
        ),
        migrations.AlterField(
            model_name='nrxcgcoeff',
            name='xcg_c2',
            field=models.FloatField(help_text='coeficiente ordem 2: nr^2', verbose_name='Xcg água c2'),
        ),
        migrations.AlterField(
            model_name='nrxcgcoeff',
            name='xcg_c3',
            field=models.FloatField(help_text='coeficiente ordem 3: nr^3', verbose_name='Xcg água c3'),
        ),
    ]
