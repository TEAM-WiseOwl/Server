from rest_framework import serializers
from .models import College, Department, ForeignTestRequired, GenedCategory, RequiredCredit, SubjectDepartment, SubjectGened

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

class SubjectDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectDepartment
        fields = [
            'subject_department_id',
            'subject_department_name',
            'subject_department_professor',
            'subject_department_credit',
            'subject_department_room_date'
        ]

class SubjectGenedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGened
        fields = [
            'subject_gened_id',
            'subject_gened_name',
            'subject_gened_professor',
            'subject_gened_credit',
            'subject_gened_room_date'
        ]

class DepartmentsSerializer(serializers.ModelSerializer):
    courses = SubjectDepartmentSerializer(many=True)

    class Meta:
        model = Department
        fields = [
            'department_id',
            'department_name',
            'courses'
        ]

class GenedSerializer(serializers.ModelSerializer):
    courses = SubjectGenedSerializer(many=True)
    
    class Meta:
        model = GenedCategory
        fields = [
            'gened_category_id',
            'gened_category_name',
            'courses'
        ]

class SubjectListSerializer(serializers.Serializer):
    subject_department = DepartmentsSerializer(many=True)
    subject_generation = GenedSerializer(many=True)  

class IRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignTestRequired
        fields = ['test_name', 'test_basic_score']

class RequiredCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredCredit
        fields = ['required_credit_gubun', 'required_major_credit', 'required_double_or_minor_credit', 'required_gened_credit']


class CompletedCreditsSerializer(serializers.Serializer):
    main_major_credits = serializers.IntegerField()
    double_major_credits = serializers.IntegerField()
    minor_credits = serializers.IntegerField(allow_null=True)
    liberal_credits = serializers.IntegerField()
    elective_credits = serializers.IntegerField()