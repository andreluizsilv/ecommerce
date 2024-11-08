# Generated by Django 5.1.3 on 2024-11-08 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0015_pagamento_aprovado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cartao', models.CharField(blank=True, max_length=200, null=True)),
                ('images_cartao', models.ImageField(blank=True, null=True, upload_to='')),
                ('validade_cartao', models.CharField(blank=True, max_length=5, null=True)),
                ('cartao_cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.cliente')),
            ],
        ),
    ]
