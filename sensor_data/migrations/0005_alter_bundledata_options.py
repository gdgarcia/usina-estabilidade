# Generated by Django 3.2.4 on 2021-08-19 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor_data', '0004_alter_bundledata_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bundledata',
            options={'ordering': ('usina', 'already_converted_to_block_data', 'bundle_data'), 'verbose_name_plural': 'Pacotes de Dados'},
        ),
    ]