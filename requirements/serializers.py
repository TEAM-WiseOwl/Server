from rest_framework import serializers
from .models import College, Department, GenedCategory

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name']

class CollegeSerializer(serializers.ModelSerializer):
    majors = DepartmentSerializer(source='department_set', many=True)  # ForeignKey 관계 활용

    class Meta:
        model = College
        fields = ['college_id', 'college_name', 'majors']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name']

class GenedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenedCategory
        fields = ['gened_category_id', 'gened_category_name']
