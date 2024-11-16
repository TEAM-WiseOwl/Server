from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from requirements.models import *
from accounts.models import *

@api_view(['GET'])
@permission_classes([AllowAny])
def main_view(self, request):
    
    user = request.user
    profile = Profile.objects.get(user_id = user)

    major_department = profile.major
    double_minor_department = profile.double_or_minor

    major_credit_completed = calculate_completed_credit_major(user, major_department)
    double_minor_credit_completed = calculate_completed_credit_double_minor(user, double_minor_department)

    major_credit_required = calculate_required_credits(profile,major_department, "major")
    double_credit_required = calculate_required_credits(profile, double_minor_department, "double")

    major_requirements = get_graduation_requirements(major_department, "본전공")
    double_requirements = get_graduation_requirements(double_minor_department, "이중전공") if double_minor_department else []

    dashboard_data = {
        "name" : profile.profile_name,
        "major" : major_department.department_name,
        "double_major" : double_minor_department.department_name if double_minor_department else None,
        "major_credit_completed" : major_credit_completed,
        "major_credit_required" : major_credit_required,
        "major_requirements" : major_requirements,
        "double_credit_completed" : double_minor_credit_completed,
        "double_credit_required" : double_credit_required,
        "double_requirements" : double_requirements

    }

    buildings = Builiding.objects.all()
    building_serializer = BuildingSerializer(buildings, many=True)


    notices = []
    notice_serializer = NoticeSerializer(notices, many=True)

    response_data = {
        "dashboard" : dashboard_data,
        "building_list" : building_serializer.data,
        "notice_list" : notice_serializer.data
    }

    ###전공과목 이수 학점
    def calculate_completed_credit_major(user, major_department):
        completed_list = MajorSubjectCompleted.objects.filter(
            user=user, 
            subject_department__department = major_department)
        
        credit = sum(completed_subject.subject_department.subject_department_credit for completed_subject in completed_list)
        return credit
    ##이중(부)전공과목 이수 학점
    def calculate_completed_credit_double_minor(user, double_minor_department):
        completed_list = MajorSubjectCompleted.objects.filter(
            user = user, 
            subject_department__department = double_minor_department)
        credit = sum(completed_subject.subject_gened.subject_gened_credit for completed_subject in completed_list)
        return credit
    
    def calculate_required_credits(profile, department, type_):
        if not department:
            return 0
        required_credits = RequiredCredit.objects.filter(
            college = department.college,
            required_credit_gubun = profile.profile_gubun).order_by('-required_credit_sn')
        for required_credit in required_credits:
            if check_student_number_range(profile.profile_student_number, required_credit.required_credit_sn):
                if type_ == "major":
                    return required_credit.required_major_credit
                elif type_ == "double":
                    return required_credit.required_double_or_minor_credit
        return 0
    
    def check_student_number_range(profile_student_number, required_credit_sn):
        if '~' in required_credit_sn:
            parts = required_credit_sn.split('~')
            if len(parts) == 2 : #구간일 경우
                lower = parts[0].strip()
                upper = parts[1].strip() if parts[1] else None
                if lower and int(profile_student_number) >= int(lower):
                    if upper:
                        return int(profile_student_number) <= int(upper)
                    return True
                if not lower: 
                    return int(profile_student_number) <= int(upper)
        return False
    def get_graduation_requirements(department, gubun):
        requirements = Requirement.objects.filter(
            department = department,
            graduation_gubun = gubun
        ).first()
        requirements_list = []
        if requirements:
            if requirements.graduation_thesis:
                requirements_list.append("졸업논문")
            if requirements.graduation_exam:
                requirements_list.append("졸업시험")
            if requirements.graduation_project:
                requirements_list.append("졸업 프로젝트")
            if requirements.graduation_qualifications:
                extra_tests = ExtraForeignTest.objects.filter(department = department)
                for test in extra_tests:
                    requirements_list.append(test.extra_test_name)
            if requirements.graduation_subjects:
                requirements_list.append("전공 필수 과목 이수")
        return requirements_list
    
    return response_data

    
    


