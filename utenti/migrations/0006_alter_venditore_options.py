# Generated by Django 5.2.4 on 2025-07-13 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utenti', '0005_alter_acquirente_options_alter_venditore_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venditore',
            options={'permissions': [('puo_visualizzare_profilo_venditore', 'Può visualizzare il profilo del venditore'), ('puo_modificare_profilo_venditore', 'Può modificare il profilo del venditore')]},
        ),
    ]
