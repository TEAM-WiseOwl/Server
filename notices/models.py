from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from requirements.models import Department
# Create your models here.

class Organ(models.Model):
    organ_id = models.BigAutoField(verbose_name="기관 아이디", null=False)
    organ_name=models.CharField(verbose_name="기관명")
    organ_link=models.URLField(verbose_name="기관 페이지 url", max_length=200)

class Notice(models.Model):
    notice_id = models.BigAutoField(verbose_name="알림 고유번호",null=False, primary_key=True)
    notice_organ_id = models.ForeignKey(Organ, on_delete=models.CASCADE,null=True)
    notice_department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_id', null=True)
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notice_link=models.URLField(verbose_name="알림 url", max_length=200)
    notice_read=models.BooleanField(verbose_name="알림 읽음 여부", default = False)
    notice_title=models.CharField(verbose_name="알림 제목")
    notice_date=models.DateField(verbose_name="알림 날짜", null=False)  

class Subscribe(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribe_major=models.BooleanField(verbose_name="본전공 구독 여부", default = False)
    subscribe_double=models.BooleanField(verbose_name="이중전공 구독 여부", default = False)
    subscribe_ai=models.BooleanField(verbose_name="ai 교육원 구독 여부", default = False)
    subscribe_foreign=models.BooleanField(verbose_name="국제교류원 교육원 구독 여부", default = False)
    
