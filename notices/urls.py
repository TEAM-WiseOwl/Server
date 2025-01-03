from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("notice/", NoticePage.as_view()),
    path("mypage/", Mypage.as_view()),
    path("mypage/course-edit/", MyCourseEdit.as_view()),
    path("mypage/myinfo-edit/", MyinfoEdit.as_view()),
    path("mypage/myinfo-edit/major/", MyinfoEditMajor.as_view()),
    path("mypage/myinfo-edit/double-to-minor/", MyInfoEditGubun.as_view()),
    path("alarm/organ/", AlarmOrgan.as_view()),
    path("alarm/", NoticeAlarm.as_view()),
    path("mypage/<str:profile_gubun>/require-edit/", RequireEdit.as_view()),
    path("mypage/course-edit/only-major/", OnlyMajor.as_view()),
]