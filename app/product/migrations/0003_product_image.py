# Generated by Django 3.2.18 on 2023-03-21 18:07

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to=product.models.product_image_file_path),
        ),
    ]
