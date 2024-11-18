from rest_framework import serializers
from .models import Builiding, Facility
from notices.models import Notice, Organ
from django.conf import settings


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['facility_name', 'facility_loc', 'facility_desc']

class FacilitywithBuildingSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.building_name') 

    class Meta:
        model = Facility
        fields = ['facility_name', 'building_name', 'facility_loc']


class FacilityCategorySerializer(serializers.Serializer):
    facility_category = serializers.CharField()
    facility_list = FacilitySerializer(many=True)


class FacilityCategorywithBuildingSerializer(serializers.Serializer):
    facility_category = serializers.CharField()
    facility_list = FacilitywithBuildingSerializer(many=True)
    

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
        model = Builiding
        fields = ['building_num', 'building_name', 'facilities']
    #summary 필요

class NoticeSerializer(serializers.ModelSerializer):
    notice_department = serializers.SerializerMethodField()
    
    class Meta:
        model = Notice
        fields = ['notice_department', 'notice_title', 'notice_date', 'notice_link']
    
    def get_notice_department(self, obj):
    # department가 존재하는지 안전하게 확인
        if hasattr(obj, 'department') and obj.department:
            return obj.department.department_name
        elif hasattr(obj, 'notice_organ') and obj.notice_organ:
            return obj.notice_organ.organ_name
        return None  # 둘 다 없는 경우


