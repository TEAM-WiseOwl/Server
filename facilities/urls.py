from django.urls import path, include
from .views import *

app_name = 'facilities'

urlpatterns = [
    path('main/', views.main_view, name='main'),  # 원하는 뷰에 매핑
]