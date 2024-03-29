# Generated by Django 3.2.4 on 2021-08-25 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_bloco_cota_terreno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usina',
            name='nome',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='bloco',
            unique_together={('nome', 'usina')},
        ),
        migrations.AlterUniqueTogether(
            name='blocodata',
            unique_together={('data', 'bloco')},
        ),
    ]
