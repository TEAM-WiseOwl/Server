from django.urls import path, include
from .views import *

app_name = 'products'

urlpatterns = [
    path('cart/', cart_view, name='cart_view'),
    path('<int:product_id>/', products_cart_view, name='products_cart_view'),
    path('<str:facility_id>/', products_view, name='products_view'),
]