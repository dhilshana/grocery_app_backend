# Generated by Django 5.1.2 on 2024-12-03 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0005_cart_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_image',
            field=models.URLField(verbose_name='image'),
        ),
    ]