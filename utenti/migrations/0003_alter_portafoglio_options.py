# Generated by Django 5.2.4 on 2025-07-13 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utenti', '0002_rename_utente_acquirente'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portafoglio',
            options={'permissions': [('puo_aggiungere_credito', 'Può inserire codice carta per aggiungere credito')]},
        ),
    ]
