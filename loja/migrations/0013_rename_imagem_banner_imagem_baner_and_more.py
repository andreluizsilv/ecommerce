# Generated by Django 5.0.6 on 2024-05-20 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0012_rename_imagem_baner_banner_imagem_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='imagem',
            new_name='imagem_baner',
        ),
        migrations.RenameField(
            model_name='banner',
            old_name='link_destino',
            new_name='links_destino',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='nome',
            new_name='nome_cliente',
        ),
        migrations.RenameField(
            model_name='produto',
            old_name='nome',
            new_name='nome_produto',
        ),
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tipo',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
    ]
