# Generated by Django 4.2.4 on 2023-08-31 18:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelBinanceArticle',
            fields=[
                ('url', models.URLField(null=True)),
                ('html', models.CharField(max_length=25000, null=True)),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('alert_priority', models.CharField(choices=[('LOW', 'LOW'), ('HIGH', 'HIGH')], max_length=50, null=True)),
                ('alert_category', models.CharField(choices=[('SWAP', 'swap'), ('NETWORK', 'network'), ('UPGRADE', 'upgrade'), ('PROTOCOL', 'protocol'), ('HARD_FORK', 'hard'), ('FORK', 'fork'), ('CEASE_TRADING', 'cease'), ('TOKEN_DELISTING', 'delist'), ('TOKEN_REMOVAL', 'removal'), ('CONTRACT_UPGRADE', 'contract'), ('SUSPENDED', 'suspended'), ('MIGRATION', 'migration'), ('CONGESTION', 'congestion'), ('SUSPENSION', 'suspension')], max_length=50, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelBinanceArticleRaw',
            fields=[
                ('release_date', models.BigIntegerField()),
                ('title', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=100)),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelBinanceEvent',
            fields=[
                ('ms_teams_message', models.JSONField(null=True)),
                ('id', models.IntegerField()),
                ('new_token_created', models.BooleanField(default=False)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.BigIntegerField(primary_key=True, serialize=False)),
                ('alert_priority', models.CharField(choices=[('LOW', 'LOW'), ('HIGH', 'HIGH')], max_length=50)),
                ('h_spot_tickers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, null=True, size=None)),
                ('h_usdm_tickers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, null=True, size=None)),
                ('l_spot_tickers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, null=True, size=None)),
                ('l_usdm_tickers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, null=True, size=None)),
                ('important_dates', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None)),
                ('networks', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None)),
                ('alert_category', models.CharField(choices=[('SWAP', 'swap'), ('NETWORK', 'network'), ('UPGRADE', 'upgrade'), ('PROTOCOL', 'protocol'), ('HARD_FORK', 'hard'), ('FORK', 'fork'), ('CEASE_TRADING', 'cease'), ('TOKEN_DELISTING', 'delist'), ('TOKEN_REMOVAL', 'removal'), ('CONTRACT_UPGRADE', 'contract'), ('SUSPENDED', 'suspended'), ('MIGRATION', 'migration'), ('CONGESTION', 'congestion'), ('SUSPENSION', 'suspension')], max_length=50)),
            ],
            options={
                'ordering': ['-release_date'],
                'managed': True,
            },
        ),
    ]
