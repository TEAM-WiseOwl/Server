from django.urls import path, include
from .views import *

app_name = 'requirements'

urlpatterns = [
    path('colleges/', CollegeListAPIView.as_view(), name=''),
    path('colleges/<str:subject_semester>/division/', SubjectDivisionAPIView.as_view()),
    path('colleges/<str:subject_semester>/subjects/', SubjectAPIView.as_view()),
]