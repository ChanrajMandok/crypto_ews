# Generated by Django 4.2.4 on 2023-08-31 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('binance_ews_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modelbinanceevent',
            options={'ordering': ['-release_date']},
        ),
    ]