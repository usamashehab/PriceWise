# Generated by Django 4.1.7 on 2023-06-22 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desired_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('price_change_notified', models.BooleanField(default=False)),
                ('notify_when_any_drop', models.BooleanField(default=False)),
                ('last_notified_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
