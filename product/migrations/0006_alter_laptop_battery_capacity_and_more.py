# Generated by Django 4.1.7 on 2023-04-25 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_rating_product_reviews_product_views_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='battery_capacity',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='battery_life',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='cpu_brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='cpu_cache_memory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='cpu_num_cores',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='cpu_num_threads',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='cpu_series',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='gpu_brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='gpu_memory',
            field=models.PositiveSmallIntegerField(blank=True, help_text='The amount of memory on the GPU in GB', null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='gpu_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='ram',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='ram_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='storage',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='storage_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='battery_capacity',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='battery_life',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='cpu_brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='cpu_cache_memory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='cpu_num_cores',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='cpu_num_threads',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='cpu_series',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='gpu_brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='gpu_memory',
            field=models.PositiveSmallIntegerField(blank=True, help_text='The amount of memory on the GPU in GB', null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='gpu_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='ram',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='ram_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='storage',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='storage_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='battery_capacity',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='battery_life',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='cpu_brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='cpu_cache_memory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='cpu_num_cores',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='cpu_num_threads',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='cpu_series',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='gpu_brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='gpu_memory',
            field=models.PositiveSmallIntegerField(blank=True, help_text='The amount of memory on the GPU in GB', null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='gpu_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='ram',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='ram_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='storage',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='storage_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tv',
            name='gpu_brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tv',
            name='gpu_memory',
            field=models.PositiveSmallIntegerField(blank=True, help_text='The amount of memory on the GPU in GB', null=True),
        ),
        migrations.AlterField(
            model_name='tv',
            name='gpu_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
