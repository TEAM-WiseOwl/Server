from django.db import models

# Create your models here.

class Builidng(models.Model):
    building_num = models.IntegerField(verbose_name='건물번호', primary_key = True)
    building_name = models.CharField(verbose_name='건물명', max_length=30, unique=True)


class Facility(models.Model):
    facility_id = models.CharField(verbose_name='편의시설 아이디', max_length = 10, primary_key=True)
    building = models.ForeignKey('Building', verbose_name = '건물번호', on_delete = models.CASCADE)
    facility_category = models.CharField(verbose_name = '편의시설 카테고리', max_length = 10)
    facility_name = models.CharField(verbose_name = '시설명', max_length = 20)
    facility_loc = models.CharField(verbose_name = '층수', max_length = 5)
    facility_desc = models.CharField(verbose_name = '시설 설명', max_length = 30)