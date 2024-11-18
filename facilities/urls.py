from django.urls import path, include
from . import views

app_name = 'facilities'

urlpatterns = [
    path('main/', views.main_view, name='main'),  # 원하는 뷰에 매핑
    path('facilities/facility_moeum/', views.facility_sub_view, name='facility_moeum'),
]