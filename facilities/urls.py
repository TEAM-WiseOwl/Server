from django.urls import path, include
from . import views

app_name = 'facilities'

urlpatterns = [
    path('main/', views.main_view, name='main'),  # 원하는 뷰에 매핑
]