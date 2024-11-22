from django.urls import path, include
from .views import *

app_name = 'requirements'

urlpatterns = [
    path('colleges/', CollegeListAPIView.as_view(), name=''),
    path('colleges/<str:subject_semester>/division/', SubjectDivisionAPIView.as_view()),
    path('colleges/<str:subject_semester>/subjects/', SubjectAPIView.as_view()),
    path('colleges/<int:subject_department_id>/department/subjects/add/', AddDepartmentSubAPIView.as_view()),
    path('colleges/<int:subject_gened_id>/gened/subjects/add/', AddGenSubAPIView.as_view()),
    path('i/', IRequirementsAPIView.as_view()),
    path('graph/', GraduationProgressAPIView.as_view()),
]