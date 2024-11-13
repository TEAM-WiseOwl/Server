# Generated by Django 4.2 on 2024-11-13 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("facilities", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "cart_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="장바구니 아이디"
                    ),
                ),
                ("cart_price", models.PositiveIntegerField(verbose_name="장바구니 총 금액")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "product_category_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="상품 카테고리 아이디"
                    ),
                ),
                (
                    "product_category_name",
                    models.CharField(max_length=20, verbose_name="상품 카테고리명"),
                ),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="facilities.facility",
                        verbose_name="편의시설 아이디",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "product_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="상품 아이디"
                    ),
                ),
                ("product_name", models.CharField(max_length=30, verbose_name="상품명")),
                ("product_price", models.PositiveIntegerField(verbose_name="상품 가격")),
                ("product_img", models.ImageField(upload_to="products")),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="facilities.facility",
                        verbose_name="편의시설 아이디",
                    ),
                ),
                (
                    "product_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.productcategory",
                        verbose_name="상품 카테고리 아이디",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CartProducts",
            fields=[
                (
                    "cart_products_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="장바구니 물품 아이디"
                    ),
                ),
                ("product_cnt", models.PositiveIntegerField(verbose_name="상품 수량")),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.cart"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
