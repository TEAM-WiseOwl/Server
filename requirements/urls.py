from django.urls import path, include
from .views import *

app_name = 'requirements'

urlpatterns = [
    path('colleges/', CollegeListAPIView.as_view(), name=''),
]