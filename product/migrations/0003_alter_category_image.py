# Generated by Django 4.1.7 on 2023-05-10 15:45

from django.db import migrations, models
import product.models.category


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_laptop_cpu_cache_memory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to=product.models.category.categor_image_path),
        ),
    ]