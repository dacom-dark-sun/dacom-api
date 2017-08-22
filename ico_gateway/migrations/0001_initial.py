# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 16:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallet', '0001_initial'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcoInvest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=10, default=0, max_digits=19, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IcoProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, null=True, unique=True)),
                ('asset_name', models.CharField(max_length=3, null=True, unique=True)),
                ('distribution_period', models.CharField(choices=[('week', 'Неделя'), ('month', 'Месяц')], default='week', max_length=20, null=True)),
                ('distribution_count', models.IntegerField(default=0, verbose_name='Количество токенов на период')),
                ('community', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='community.Community')),
            ],
        ),
        migrations.CreateModel(
            name='IcoWallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ico_project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ico_gateway.IcoProject')),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ico_wallet', to='wallet.Wallet')),
            ],
        ),
        migrations.AddField(
            model_name='icoinvest',
            name='ico_wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ico_gateway.IcoWallet'),
        ),
        migrations.AlterUniqueTogether(
            name='icowallet',
            unique_together=set([('ico_project', 'wallet')]),
        ),
    ]
