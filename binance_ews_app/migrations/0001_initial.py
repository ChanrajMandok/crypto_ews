# Generated by Django 4.2.4 on 2023-08-24 16:42

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
                ('alert_priority', models.CharField(choices=[('HIGH', 'HIGH'), ('LOW', 'LOW')], max_length=50, null=True)),
                ('alert_category', models.CharField(choices=[('CONTRACT', 'contract'), ('PROTOCOL', 'protocol'), ('NETWORK', 'network'), ('UPGRADE', 'upgrade'), ('SWAP', 'swap'), ('CONGESTION', 'congestion'), ('SUSPENDED', 'suspended'), ('SUSPENSION', 'suspension'), ('MIGRATION', 'migration'), ('DELIST', 'delist'), ('HARD', 'hard'), ('FORK', 'fork'), ('CEASE', 'cease'), ('REMOVAL', 'removal')], max_length=50, null=True)),
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
                ('release_date', models.BigIntegerField()),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('article_text', models.TextField(max_length=25000)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('alert_priority', models.CharField(choices=[('HIGH', 'HIGH'), ('LOW', 'LOW')], max_length=50)),
                ('important_dates', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None)),
                ('alert_category', models.CharField(choices=[('CONTRACT', 'contract'), ('PROTOCOL', 'protocol'), ('NETWORK', 'network'), ('UPGRADE', 'upgrade'), ('SWAP', 'swap'), ('CONGESTION', 'congestion'), ('SUSPENDED', 'suspended'), ('SUSPENSION', 'suspension'), ('MIGRATION', 'migration'), ('DELIST', 'delist'), ('HARD', 'hard'), ('FORK', 'fork'), ('CEASE', 'cease'), ('REMOVAL', 'removal')], max_length=50)),
            ],
            options={
                'managed': False,
            },
        ),
    ]