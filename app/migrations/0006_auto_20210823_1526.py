# Generated by Django 3.2.4 on 2021-08-23 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210729_1256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bloco',
            options={'ordering': ('usina', 'nome')},
        ),
        migrations.AlterModelOptions(
            name='blocodata',
            options={'ordering': ('bloco', 'data'), 'verbose_name': 'dados de bloco', 'verbose_name_plural': 'dados de blocos'},
        ),
    ]
