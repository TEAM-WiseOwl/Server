from rest_framework import serializers
from accounts.models import *
from requirements.models import *
from collections import defaultdict

class MypageSerializer(serializers.ModelSerializer):
  department_name = serializers.SerializerMethodField()
  double_minor_department_name = serializers.SerializerMethodField()
  class Meta:
    model = Profile
    fields = ['profile_name', 'profile_student_number', 'profile_grade', 'major','double_major']
  
  def get_major(self, obj):
    major_department = Department.objects.get(department_id=obj.major_id)
    return major_department.department_name
  def get_double_major(self, obj):
    double_minor_department = Department.objects.get(department_id=obj.double_minor_id)
    return double_minor_department.department_name
  
  class MyInfoSerializer(serializers.ModelSerializer):
    college = serializers.SerializerMethodField()
    major = serializers.SerializerMethodField()
    double_college = serializers.SerializerMethodField()
    double_major = serializers.SerializerMethodField()
    class Meta:
      model = Profile
      field=['college', 'major', 'double_college', 'double_major', 'profile_gubun' ]

    def get_college(self, obj):
      major_college = College.objects.get(college_id=obj.major_college_id)
      return major_college.college_name
    def get_major(self, obj):
      major = Department.objects.get(department_id=obj.major_id)
      return major.department_name
    def get_double_college(self, obj):
      double_college=College.objects.get(college_id=obj.double_or_minor_college_id)
      return double_college.college_name
    
    def get_double_major(self, obj):
      double_major=Department.objects.get(department_id=obj.double_or_minor_id)
      return double_major.department_name
    

class CourseSubjectSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    grade = serializers.CharField()
    retry_yn = serializers.BooleanField()
    credit = serializers.IntegerField()

class CourseYearSerializer(serializers.Serializer):
    complete_year = serializers.CharField()
    school_year = serializers.IntegerField()
    course_subject = CourseSubjectSerializer(many=True)

class CourseCompleteSerializer(serializers.ModelSerializer):
  double_major = serializers.SerializerMethodField()
  major = serializers.SerializerMethodField()
  course = serializers.SerializerMethodField()
  class Meta:
    field=['major','profile_gubun', 'second_major', 'complete_year', 'course' ]
  def get_major(self, obj):
      major = Department.objects.get(department_id=obj.major_id)
      return major.department_name
  def get_double_major(self, obj):
      double_major=Department.objects.get(department_id=obj.double_or_minor_id)
      return double_major.department_name
  def get_course(self, obj):
        major_subjects = MajorSubjectCompleted.objects.filter(user=obj.user)
        general_subjects = GeneralSubjectCompleted.objects.filter(user=obj.user)

        # 결과를 그룹화할 dict 초기화
        courses_by_year = defaultdict(lambda: {
            'complete_year': None,
            'school_year': None,
            'course_subject': []
        })

        # MajorSubjectCompleted 모델을 complete_year, school_year로 묶어서 데이터 준비
        for major_subject in major_subjects:
            key = (major_subject.completed_year, major_subject.school_year)
            courses_by_year[key]['complete_year'] = major_subject.completed_year
            courses_by_year[key]['school_year'] = major_subject.school_year
            courses_by_year[key]['course_subject'].append({
                'subject_name': major_subject.subject_department.subject_name,
                'grade': major_subject.grade,
                'retry_yn': major_subject.retry_yn,
                'credit': major_subject.subject_department.credit
            })

        # GeneralSubjectCompleted 모델을 complete_year, school_year로 묶어서 데이터 준비
        for general_subject in general_subjects:
            key = (general_subject.completed_year, general_subject.school_year)
            courses_by_year[key]['complete_year'] = general_subject.completed_year
            courses_by_year[key]['school_year'] = general_subject.school_year
            courses_by_year[key]['course_subject'].append({
                'subject_name': general_subject.subject_gened.subject_name,
                'grade': general_subject.grade,
                'retry_yn': general_subject.retry_yn,
                'credit': general_subject.subject_gened.credit
            })

        # courses_by_year를 리스트로 반환
        return [CourseYearSerializer(data=course).data for course in courses_by_year.values()]

