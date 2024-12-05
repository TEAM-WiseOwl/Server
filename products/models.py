from django.db import models
from django.contrib.auth import get_user_model 
from facilities.models import Facility
from django.conf import settings

class ProductCategory(models.Model):
    product_category_id = models.BigAutoField(verbose_name='상품 카테고리 아이디',primary_key = True)
    facility = models.ForeignKey(Facility, verbose_name = '편의시설 아이디', on_delete = models.CASCADE)
    product_category_name = models.CharField(verbose_name = '상품 카테고리명', max_length = 20)

class Product(models.Model):
    product_id = models.BigAutoField(verbose_name = '상품 아이디', primary_key = True )
    product_category = models.ForeignKey('ProductCategory', verbose_name = '상품 카테고리 아이디', on_delete = models.CASCADE)
    facility = models.ForeignKey(Facility, verbose_name = '편의시설 아이디', on_delete = models.CASCADE)
    product_name = models.CharField(verbose_name = '상품명', max_length = 30)
    product_price = models.PositiveIntegerField(verbose_name = '상품 가격')
    product_img = models.CharField(verbose_name = '상품이미지', max_length = 700)

class Cart(models.Model):
    cart_id = models.BigAutoField(verbose_name = '장바구니 아이디', primary_key = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.
    CASCADE, null = False)
    cart_price = models.PositiveIntegerField(verbose_name = '장바구니 총 금액')

class CartProducts(models.Model):
    cart_products_id = models.BigAutoField(verbose_name = '장바구니 물품 아이디', primary_key = True)
    cart = models.ForeignKey('Cart', on_delete = models.CASCADE)
    product = models.ForeignKey('Product', on_delete = models.CASCADE)
    product_cnt = models.PositiveIntegerField(verbose_name = '상품 수량')




