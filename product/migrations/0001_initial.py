# Generated by Django 4.1.7 on 2023-05-11 23:02

import datetime
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import product.models.category


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(upload_to=product.models.category.categor_image_path)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('description', models.TextField(null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('brand', models.CharField(max_length=50, null=True)),
                ('available', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('uid', models.CharField(max_length=255)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('reviews', models.PositiveIntegerField(default=0)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category')),
            ],
            options={
                'ordering': ['-views', '-rating'],
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Amazon', 'Amazon'), ('Jumia', 'Jumia'), ('Noon', 'Noon')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255, null=True)),
                ('connectivity_tech', models.CharField(blank=True, max_length=50, null=True)),
                ('display_type', models.CharField(blank=True, max_length=50, null=True)),
                ('display_size', models.CharField(blank=True, max_length=50, null=True)),
                ('display_resolution', models.CharField(blank=True, max_length=50, null=True)),
                ('refresh_rate', models.CharField(blank=True, max_length=10, null=True)),
                ('smart_tv', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255, null=True)),
                ('operating_system', models.CharField(blank=True, max_length=50, null=True)),
                ('connectivity_tech', models.CharField(blank=True, max_length=50, null=True)),
                ('display_type', models.CharField(blank=True, max_length=50, null=True)),
                ('display_size', models.CharField(blank=True, max_length=50, null=True)),
                ('display_resolution', models.CharField(blank=True, max_length=50, null=True)),
                ('refresh_rate', models.CharField(blank=True, max_length=10, null=True)),
                ('battery_capacity', models.CharField(max_length=50, null=True)),
                ('battery_life', models.CharField(max_length=50, null=True)),
                ('storage', models.CharField(max_length=10, null=True)),
                ('ram', models.CharField(max_length=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.vendor'),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(default=datetime.date.today)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='product.product')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255, null=True)),
                ('operating_system', models.CharField(blank=True, max_length=50, null=True)),
                ('connectivity_tech', models.CharField(blank=True, max_length=50, null=True)),
                ('display_type', models.CharField(blank=True, max_length=50, null=True)),
                ('display_size', models.CharField(blank=True, max_length=50, null=True)),
                ('display_resolution', models.CharField(blank=True, max_length=50, null=True)),
                ('refresh_rate', models.CharField(blank=True, max_length=10, null=True)),
                ('battery_capacity', models.CharField(max_length=50, null=True)),
                ('battery_life', models.CharField(max_length=50, null=True)),
                ('storage', models.CharField(max_length=10, null=True)),
                ('ram', models.CharField(max_length=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255, null=True)),
                ('operating_system', models.CharField(blank=True, max_length=50, null=True)),
                ('display_type', models.CharField(blank=True, max_length=50, null=True)),
                ('display_size', models.CharField(blank=True, max_length=50, null=True)),
                ('display_resolution', models.CharField(blank=True, max_length=50, null=True)),
                ('refresh_rate', models.CharField(blank=True, max_length=10, null=True)),
                ('cpu_brand', models.CharField(max_length=100, null=True)),
                ('cpu_type', models.CharField(max_length=100, null=True)),
                ('cpu_speed', models.CharField(max_length=50, null=True)),
                ('cpu_num_cores', models.CharField(max_length=10, null=True)),
                ('gpu_brand', models.CharField(help_text='The type of GPU chip (e.g. NVIDIA, AMD)', max_length=100, null=True)),
                ('gpu_coprocessor', models.CharField(help_text='The model of a specific type (e.g AMD Radeon Graphics, ..)', max_length=100, null=True)),
                ('gpu_memory', models.CharField(help_text='The amount of memory on the GPU in GB', max_length=10, null=True)),
                ('battery_capacity', models.CharField(max_length=50, null=True)),
                ('battery_life', models.CharField(max_length=50, null=True)),
                ('storage', models.CharField(max_length=10, null=True)),
                ('ram', models.CharField(max_length=10, null=True)),
                ('storage_type', models.CharField(default='HDD', max_length=50, null=True)),
                ('ram_type', models.CharField(max_length=50, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=50)),
                ('order', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='product_pro_search__e78047_gin'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('vendor', 'uid')},
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('product', 'order')},
        ),
    ]
