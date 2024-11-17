from rest_framework import serializers
from accounts.models import *
from requirements.models import *
from .models import *
from collections import defaultdict

class MypageSerializer(serializers.ModelSerializer):
  major = serializers.SerializerMethodField()
  double_major = serializers.SerializerMethodField()
  class Meta:
    model = Profile
    fields = ['profile_name', 'profile_student_number', 'profile_grade', 'major','double_major']
  
  def get_major(self, obj):
    major_department = Department.objects.get(department_id=obj.major_id)
    return major_department.department_name
  def get_double_major(self, obj):
    double_minor_department = Department.objects.get(department_id=obj.double_or_minor_id)
    return double_minor_department.department_name
  
class MyInfoSerializer(serializers.ModelSerializer):
  college = serializers.SerializerMethodField()
  major = serializers.SerializerMethodField()
  double_college = serializers.SerializerMethodField()
  double_major = serializers.SerializerMethodField()
  class Meta:
    model = Profile
    fields=['college', 'major', 'double_college', 'double_major', 'profile_gubun' ]

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
  second_major = serializers.SerializerMethodField()
  major = serializers.SerializerMethodField()
  course = serializers.SerializerMethodField()
  class Meta:
    model=Profile
    fields=['major','profile_gubun', 'second_major', 'course' ]
  def get_major(self, obj):
      major = Department.objects.get(department_id=obj.major_id)
      return major.department_name
  def get_second_major(self, obj):
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
                'subject_name': major_subject.subject_department.subject_department_name,
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
                'subject_name': general_subject.subject_gened.subject_gened_name,
                'grade': general_subject.grade,
                'retry_yn': general_subject.retry_yn,
                'credit': general_subject.subject_gened.subject_gened_credit
            })

        # courses_by_year를 리스트로 반환
        serialized_courses = []
        for course in courses_by_year.values():
           course_serializer = CourseYearSerializer(data=course)
           if course_serializer.is_valid():
              serialized_courses.append(course_serializer.data)
           else:
              print(course_serializer.errors)  # 유효하지 않은 데이터에 대한 오류 출력

        return serialized_courses


class SubscribeOrganSerializer(serializers.ModelSerializer):
   organ = serializers.SerializerMethodField()
   class Meta:
        model = Subscribe
        fields = ['organ'] 
   def get_organ(self, obj):
      organs = []
      profile = Profile.objects.filter(user_id=obj.user_id).first()
      if profile:
         if profile.major_id:
          major = Department.objects.filter(department_id=profile.major_id).first()
          if major:
             organs.append({"organ_name": major.department_name, "subscribe_yn": True})
         if profile.double_or_minor_id:
                double_major = Department.objects.filter(department_id=profile.double_or_minor_id).first()
                if double_major:
                    organs.append({"organ_name": double_major.department_name, "subscribe_yn": True})
         organs.append({"organ_name": "AI 교육원", "subscribe_yn": True})
         organs.append({"organ_name": "국제교류팀 교육원", "subscribe_yn": True})
         organs.append({"organ_name": "진로취업지원센터", "subscribe_yn": True})
         organs.append({"organ_name": "특수외국어교육진흥원", "subscribe_yn": True})
         organs.append({"organ_name": "FLEX 센터", "subscribe_yn": True})
         organs.append({"organ_name": "외국어교육센터", "subscribe_yn": True})
      return organs
        
