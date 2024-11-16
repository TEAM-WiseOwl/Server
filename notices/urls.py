from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("basket/", Notice.as_view()),
    path("mypage/<int:user_id>/", Mypage.as_view()),
]