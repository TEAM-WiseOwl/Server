from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from requirements.models import *
from accounts.models import *
from notices.models import *
from django.db.models import Q
from .models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def main_view(request):
    
    user = request.user
    profile = Profile.objects.get(user_id = user)

    major_department = profile.major
    double_minor_department = profile.double_or_minor

    major_credit_completed = calculate_completed_credit_major(user, major_department)
    double_minor_credit_completed = calculate_completed_credit_double_minor(user, double_minor_department)


    major_credit_required = calculate_required_credits(profile,major_department, "major")
    double_credit_required = calculate_double_minor_credits(profile, major_department)

    major_requirements = get_graduation_requirements(major_department, "본전공")
    double_requirements = get_graduation_requirements(double_minor_department, "이중전공") if double_minor_department else []

    dashboard_data = {
        "name" : profile.profile_name,
        "gubun" : profile.profile_gubun,
        "major" : major_department.department_name,
        "double_major" : double_minor_department.department_name if double_minor_department else None,
        "major_credit_completed" : major_credit_completed,
        "major_credit_required" : major_credit_required,
        "major_requirements" : major_requirements,
        "double_credit_completed" : double_minor_credit_completed,
        "double_credit_required" : double_credit_required,
        "double_requirements" : double_requirements

    }


    buildings = Builiding.objects.all().order_by('building_num')
    building_list = []


    for building in buildings:
        facilities = building.facility_set.all()
        if not facilities.exists():
            print(f"No facilities found for building: {building.building_name}")
            continue  # 다음 건물로 이동

        total_facilities = facilities.count()
        category_counts = {
            "restaurant_cafe": facilities.filter(facility_category='카페/식당').count(),
            "convenience_store": facilities.filter(facility_category='편의점').count(),
            "reading_room": facilities.filter(facility_category='열람실').count(),
            "computer_copier": facilities.filter(facility_category='컴퓨터/복사기').count(),
            "etc": facilities.filter(facility_category='기타').count(),
        }

        facility_set = FacilityCategorySerializer(
            [
                {
                    "facility_category" : "전체",
                    "facility_list" : FacilitySerializer(facilities, many=True).data
                },
                {
                    "facility_category" : "카페/식당",
                    "facility_list" : FacilitySerializer(facilities.filter(facility_category = '카페/식당'), many = True).data
                },
                {
                    "facility_category" : "편의점",
                    "facility_list" : FacilitySerializer(facilities.filter(facility_category = '편의점'), many = True).data
                },
                {
                    "facility_category" : "열람실",
                    "facility_list" : FacilitySerializer(facilities.filter(facility_category = '열람실'), many = True).data
                },
                {
                    "facility_category" : "컴퓨터/복사기",
                    "facility_list" : FacilitySerializer(facilities.filter(facility_category = '컴퓨터/복사기'), many = True).data
                },
                {
                    "facility_category" : "기타",
                    "facility_list" : FacilitySerializer(facilities.filter(facility_category = '기타'), many = True).data
                }

            ],many = True
        ).data


        facilities_summary = {
            "total": total_facilities,
            "restaurant_cafe": category_counts["restaurant_cafe"],
            "convenience_store": category_counts["convenience_store"],
            "reading_room": category_counts["reading_room"],
            "computer_copier": category_counts["computer_copier"],
            "etc": category_counts["etc"],
            "facility_set": facility_set
        }
        building_data = {
            "building_num": building.building_num,
            "building_name": building.building_name,
            "facilities_summary": facilities_summary
        }
        building_list.append(building_data)



    # 공지사항 조회: user_id 기준으로 날짜순 정렬 후 최근 3개만 가져오기
    notices = Notice.objects.filter(user_id=user).order_by('-notice_date')[:3]

    # 공지사항이 없을 경우 빈 리스트로 처리
    if not notices:
        notices = []

    # 공지사항 시리얼라이저 생성
    notice_serializer = NoticeSerializer(notices, many=True)


    response_data = {
        "dashboard" : dashboard_data,
        "building_list" : building_list,
        "notice_list" : notice_serializer.data
    }

    grades_queryset = MajorSubjectCompleted.objects.filter(user=user).union(
            GeneralSubjectCompleted.objects.filter(user=user)
        )
    total_credits = 0
    total_points = 0

    for record in grades_queryset:
        grade = record.grade
        credits = (
            record.subject_department.subject_department_credit
            if hasattr(record, "subject_department")
            else record.subject_gened.subject_gened_credit
        )
        if grade == "P":
            continue

        grade_points = {"A+": 4.5, "A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D":1.0, "F": 0.0}.get(grade, 0)
        total_points += grade_points * credits
        total_credits += credits

    profile.profile_grade = round(total_points / total_credits, 2) if total_credits > 0 else 0
    profile.save()
    return Response(response_data)

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
    
    credit = sum(completed_subject.subject_department.
    subject_department_credit for completed_subject in completed_list)

    return credit

def calculate_required_credits(profile, department, type_):
    if not department:
        return 0
    required_credits = RequiredCredit.objects.filter(
        college=department.college,
        required_credit_gubun=profile.profile_gubun).order_by('-required_credit_sn')
    for required_credit in required_credits:
        if check_student_number_range(profile.profile_student_number, required_credit.required_credit_sn):
            if type_ == "major":
                return required_credit.required_major_credit
    return 0

def calculate_double_minor_credits(profile, major_department):
    if not major_department:
        return 0
    required_credits = RequiredCredit.objects.filter(
        college=major_department.college).order_by('-required_credit_sn')
    for required_credit in required_credits:
        if check_student_number_range(profile.profile_student_number, required_credit.required_credit_sn):
            if profile.profile_gubun in ['이중전공', '부전공']:
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




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def facility_sub_view(request):
    facilities = Facility.objects.all()

    # 카테고리별 데이터 생성
    categories = [
        {
            "facility_category": "전체",
            "facility_list": facilities
        },
        {
            "facility_category": "카페/식당",
            "facility_list": facilities.filter(facility_category='카페/식당')
        },
        {
            "facility_category": "편의점",
            "facility_list": facilities.filter(facility_category='편의점')
        },
        {
            "facility_category": "열람실",
            "facility_list": facilities.filter(facility_category='열람실')
        },
        {
            "facility_category": "컴퓨터/복사기",
            "facility_list": facilities.filter(facility_category='컴퓨터/복사기')
        },
        {
            "facility_category": "기타",
            "facility_list": facilities.filter(facility_category='기타')
        }
    ]

    # 직렬화
    facility_set = FacilityCategorywithBuildingSerializer(categories, many=True).data

    response_data = {
        "total": facilities.count(),
        "restaurant_cafe": facilities.filter(facility_category='카페/식당').count(),
        "convenience_store": facilities.filter(facility_category='편의점').count(),
        "reading_room": facilities.filter(facility_category='열람실').count(),
        "computer_copier": facilities.filter(facility_category='컴퓨터/복사기').count(),
        "etc": facilities.filter(facility_category='기타').count(),
        "facility_set": facility_set
    }

    return Response(response_data)
