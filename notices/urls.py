from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("basket/<int:user_id>/", NoticePage.as_view()),
    path("mypage/<int:user_id>/", Mypage.as_view()),
    path("mypage/course-edit/<int:user_id>/", MyCourseEdit.as_view()),
    path("alarm/organ/<int:user_id>/", AlarmOrgan.as_view()),
]