# Generated by Django 4.2 on 2024-11-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_img",
            field=models.CharField(max_length=700, verbose_name="상품이미지"),
        ),
    ]