# Generated by Django 3.2.4 on 2021-07-05 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bloco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('volume_bloco', models.FloatField()),
                ('xcg_bloco', models.FloatField()),
                ('largura', models.FloatField()),
                ('comprimento', models.FloatField()),
                ('area', models.FloatField()),
                ('cota_base_montante', models.FloatField()),
                ('cota_base_jusante', models.FloatField()),
                ('cota_ogiva', models.FloatField()),
                ('cota_sedimento', models.FloatField()),
                ('cota_terreno', models.FloatField()),
                ('v_enchimento', models.FloatField()),
                ('xcg_enchimento', models.FloatField()),
                ('dist_xm', models.FloatField()),
                ('dist_xi', models.FloatField()),
                ('dist_xj', models.FloatField()),
                ('gamma_concreto', models.FloatField()),
                ('gamma_agua', models.FloatField()),
                ('gamma_enchimento', models.FloatField()),
                ('gamma_sedimento', models.FloatField()),
                ('phi', models.FloatField()),
                ('c', models.FloatField()),
                ('gamma_phi', models.FloatField()),
                ('gamma_c', models.FloatField()),
                ('angulo_sedimento', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Usina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('descricao', models.TextField(blank=True, max_length=100, null=True)),
                ('min_fst', models.FloatField(default=1.0)),
                ('min_fsd', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='NrVolCoeff',
            fields=[
                ('bloco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='nr_vol_coeff', serialize=False, to='app.bloco')),
                ('c0', models.FloatField(help_text='coeficiente ordem 0: nr^0')),
                ('c1', models.FloatField(help_text='coeficiente ordem 1: nr^1')),
                ('c2', models.FloatField(help_text='coeficiente ordem 2: nr^2')),
            ],
        ),
        migrations.CreateModel(
            name='NrXcgCoeff',
            fields=[
                ('bloco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='nr_xcg_coeff', serialize=False, to='app.bloco')),
                ('c0', models.FloatField(help_text='coeficiente ordem 0: nr^0')),
                ('c1', models.FloatField(help_text='coeficiente ordem 1: nr^1')),
                ('c2', models.FloatField(help_text='coeficiente ordem 2: nr^2')),
                ('c3', models.FloatField(help_text='coeficiente ordem 3: nr^3')),
            ],
        ),
        migrations.CreateModel(
            name='BlocoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(db_index=True)),
                ('nr', models.FloatField(help_text='nível do reservatório')),
                ('pzm', models.FloatField(help_text='piezômetro m')),
                ('pzi', models.FloatField(help_text='piezômetro i')),
                ('pzj', models.FloatField(help_text='piezômetro j')),
                ('bloco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='app.bloco')),
            ],
            options={
                'verbose_name': 'dados de bloco',
                'verbose_name_plural': 'dados de blocos',
                'ordering': ['data'],
            },
        ),
        migrations.AddField(
            model_name='bloco',
            name='usina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocos', to='app.usina'),
        ),
    ]
