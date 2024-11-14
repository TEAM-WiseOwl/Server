from rest_framework import serializers
from .models import Building, Facility
from notices.models import Notice, Organ
from django.conf import settings


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['facility_name', 'facility_loc']

class FacilityCategorySerializer(serializers.Serializer):
    facility_category = serializers.CharField()
    facility_list = FacilitySerializer(many=True)
    

class FacilitySummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    restaurant_cafe =  serializers.IntegerField()
    convenience_store = serializers.IntegerField()
    reading_room = serializers.IntegerField()
    computer_copier = serializers.IntegerField()
    etc = serializers.IntegerField()
    facility_set = FacilityCategorySerializer(many=True)

class BuildingSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, read_only=True, source='facility_set') 

    class Meta:
        model = Building
        fields = ['building_num', 'building_name', 'facilities']
    #summary 필요

class NoticeSerializer(serializers.ModelSerializer):
    notice_department = serializers.CharField(source='notice_department_id.department_name')
    notice_link = serializers.URLField()

    class Meta:
        model = Notice
        fields = ['notice_department', 'notice_title', 'notice_date', 'notice_link']

class MainResponseSerializers(serializers.Serializer):
    name = serializers.CharField()
    major = serializers.CharField()
    double_major = serializers.CharField()
    major_credit_completed = serializers.IntegerField()
    major_credit_required = serializers.IntegerField()
    major_requirements = serializers.ListField(child = serializers.CharField())
    double_credit_completed = serializers.IntegerField()
    double_credit_required = serializers.IntegerField()
    double_requirements = serializers.ListField(child = serializers.CharField())
    building_list = BuildingSerializer(many = True)
    notice_list = NoticeSerializer(many = True)
