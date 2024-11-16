from rest_framework import serializers
from accounts.models import *
from requirements.models import *

class MypageSerializezr(serializers.ModelSerializer):
  major = serializers.SerializerMethodField()
  class Meta:
    model = Profile
    fields = ['profile_name', 'profile_student_number', 'profile_grade', 'major']
  
  def get_department_name(self, obj):
    return obj.department.department_name
    