# Generated by Django 5.1.2 on 2024-12-21 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='unit',
            field=models.CharField(default='Kg', max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='unit',
            field=models.CharField(default='Kg', max_length=10),
        ),
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.URLField(blank=True, default='', null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(default=1, help_text='Rating should be between 1 and 5'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_image',
            field=models.URLField(verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_image',
            field=models.URLField(verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='product_image',
            field=models.URLField(verbose_name='image'),
        ),
    ]
