# Generated by Django 4.1.7 on 2023-05-13 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laptop',
            old_name='model',
            new_name='model_name',
        ),
        migrations.RenameField(
            model_name='mobile',
            old_name='model',
            new_name='model_name',
        ),
        migrations.RenameField(
            model_name='tablet',
            old_name='model',
            new_name='model_name',
        ),
        migrations.RenameField(
            model_name='tv',
            old_name='model',
            new_name='model_name',
        ),
    ]