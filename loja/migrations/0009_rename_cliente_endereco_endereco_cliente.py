# Generated by Django 5.0.6 on 2024-05-14 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0008_rename_cidigo_cor_codigo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='endereco',
            old_name='cliente_endereco',
            new_name='cliente',
        ),
    ]
