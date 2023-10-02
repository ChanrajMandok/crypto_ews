# Generated by Django 4.2.4 on 2023-10-02 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ews_app', '0001_initial'),
        ('binance_ews_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelBinanceEvent',
            fields=[
                ('modeleventinterface_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ews_app.modeleventinterface')),
            ],
            options={
                'ordering': ['-release_date'],
                'managed': True,
            },
            bases=('ews_app.modeleventinterface',),
        ),
    ]
