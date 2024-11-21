from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import College, ForeignTestRequired, GeneralSubjectCompleted, MajorSubjectCompleted, OpeningSemester, Department, GenedCategory, Requirement, SubjectDepartment, SubjectGened
from accounts.models import Profile
from .serializers import CollegeSerializer, DepartmentSerializer, IRequiredSerializer, GenedCategorySerializer, SubjectListSerializer

class CollegeListAPIView(APIView):
    def get(self, request):
        colleges = College.objects.prefetch_related('department_set')
        serializer = CollegeSerializer(colleges, many=True)
        return Response({"colleges": serializer.data}, status=status.HTTP_200_OK)

class SubjectDivisionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_semester):
        try:
            opening_semester = OpeningSemester.objects.filter(subject_semester=subject_semester).first()
            
            if not opening_semester:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            departments = Department.objects.all()
            
            general_education = GenedCategory.objects.filter(
                subjectgened__opening_semester=opening_semester
            ).distinct()

            department_serializer = DepartmentSerializer(departments, many=True)
            general_education_serializer = GenedCategorySerializer(general_education, many=True)

            response_data = {
                "department": department_serializer.data,
                "general_education": general_education_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SubjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_semester):
        if not subject_semester:
            return Response({"error": "subject_semester parameter is required"}, status=400)

        opening_semester = OpeningSemester.objects.filter(subject_semester=subject_semester).first()
        
        if not opening_semester:
            return Response({"error": "No subjects found for the given semester"}, status=404)

        subject_department = SubjectDepartment.objects.filter(opening_semester=opening_semester).select_related('department')

        subject_gened = SubjectGened.objects.filter(opening_semester=opening_semester).select_related('gened_category')

        departments = Department.objects.all()

        response_data = {
            "subject_department": [],
            "subject_generation": []
        }

        for department in departments:
            courses = []
            subject_dept_courses = subject_department.filter(department=department)

            for course in subject_dept_courses:
                courses.append({
                    "subject_department_id": course.subject_department_id,
                    "subject_department_name": course.subject_department_name,
                    "subject_department_professor": course.subject_department_professor,
                    "subject_department_credit": course.subject_department_credit,
                    "subject_department_room_date": course.subject_department_room_date,
                })

            if courses:
                response_data["subject_department"].append({
                    "department_id": department.department_id,
                    "department_name": department.department_name,
                    "courses": courses
                })

        for gened_category in GenedCategory.objects.all():
            gened_courses = []
            subject_gened_courses = subject_gened.filter(gened_category=gened_category)

            for course in subject_gened_courses:
                gened_courses.append({
                    "subject_gened_id": course.subject_gened_id,
                    "subject_gened_name": course.subject_gened_name,
                    "subject_gened_professor": course.subject_gened_professor,
                    "subject_gened_credit": course.subject_gened_credit,
                    "subject_gened_room_date": course.subject_gened_room_date,
                })

            if gened_courses:
                response_data["subject_generation"].append({
                    "gened_category_id": gened_category.gened_category_id,
                    "gened_category_name": gened_category.gened_category_name,
                    "courses": gened_courses
                })
        serializer = SubjectListSerializer(response_data)
        return Response(serializer.data)

class AddDepartmentSubAPIView(APIView):
    def post(self, request, subject_department_id):
        user = request.user
        
        if not subject_department_id:
            return Response({"error": "subject_department_id parameter is required"}, status=400)
        
        try:
            subject_department = SubjectDepartment.objects.get(pk=subject_department_id)
        except SubjectDepartment.DoesNotExist:
            return Response({"error": "SubjectDepartment not found"}, status=status.HTTP_404_NOT_FOUND)

        school_year = request.data.get("school_year")
        if not school_year:
            return Response({"error": "subject_department_id parameter is required"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            school_year = int(school_year)
        except ValueError:
            return Response({"error": "school_year must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        if MajorSubjectCompleted.objects.filter(user=user, subject_department=subject_department).exists():
            return Response({"error": "This subject is already completed by the user."}, status=status.HTTP_400_BAD_REQUEST)

        completed_year = subject_department.opening_semester.subject_semester
        
        major_subject_completed = MajorSubjectCompleted.objects.create(
            user=user,
            subject_department=subject_department,
            completed_year=completed_year,
            school_year=school_year
        )
        return Response({"message": "Subject added successfully!"}, status=status.HTTP_201_CREATED)

class AddGenSubAPIView(APIView):
    def post(self, request, subject_gened_id):
        user = request.user
        
        if not subject_gened_id:
            return Response({"error": "subject_gened_id parameter is required"}, status=400)
        
        try:
            subject_gened = SubjectGened.objects.get(pk=subject_gened_id)
        except SubjectGened.DoesNotExist:
            return Response({"error": "SubjectGened not found"}, status=status.HTTP_404_NOT_FOUND)

        school_year = request.data.get("school_year")
        if not school_year:
            return Response({"error": "subject_gened_id parameter is required"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            school_year = int(school_year)
        except ValueError:
            return Response({"error": "school_year must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        if GeneralSubjectCompleted.objects.filter(user=user, subject_gened=subject_gened).exists():
            return Response({"error": "This subject is already completed by the user."}, status=status.HTTP_400_BAD_REQUEST)

        completed_year = subject_gened.opening_semester.subject_semester
        
        major_subject_completed = GeneralSubjectCompleted.objects.create(
            user=user,
            subject_gened=subject_gened,
            completed_year=completed_year,
            school_year=school_year
        )
        return Response({"message": "Subject added successfully!"}, status=status.HTTP_201_CREATED)

class IRequirementsAPIView(APIView):
    def get(self, request):
        user = request.user
        
        try:
            # 유저 프로필 가져오기
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 본전공과 이중/부전공 학과 가져오기
        major_department = profile.major
        double_minor_department = profile.double_or_minor

        # 본전공 데이터
        major_requirements = Requirement.objects.filter(department=major_department).first()
        major_tests = ForeignTestRequired.objects.filter(department=major_department)

        # 이중/부전공 데이터
        double_minor_requirements = Requirement.objects.filter(department=double_minor_department).first() if double_minor_department else None
        double_minor_tests = ForeignTestRequired.objects.filter(department=double_minor_department) if double_minor_department else None

        # 응답 데이터 구조 생성
        result = {
            "major": {
                "requirement_description": major_requirements.description if major_requirements else None,
                "extra_foreign_test": None,  # 기본값을 null로 설정
                "lang_test": {
                    "basic": [],
                    "etc": []
                }
            },
            "double_or_minor": {
                "requirement_description": double_minor_requirements.description if double_minor_requirements else None,
                "extra_foreign_test": None,  # 기본값을 null로 설정
                "lang_test": {
                    "basic": [],
                    "etc": []
                }
            }
        }

        # 본전공 시험 데이터 분류
        for test in major_tests:
            test_data = IRequiredSerializer(test).data
            if test.test_name == "TOEIC" and test.test_basic_score:
                result["major"]["lang_test"]["basic"].append(test_data)
            else:
                result["major"]["lang_test"]["etc"].append(test_data)

        # 이중/부전공 시험 데이터 분류
        if double_minor_tests:
            for test in double_minor_tests:
                test_data = IRequiredSerializer(test).data
                if test.test_name == "TOEIC" and test.test_basic_score:
                    result["double_or_minor"]["lang_test"]["basic"].append(test_data)
                else:
                    result["double_or_minor"]["lang_test"]["etc"].append(test_data)

        return Response(result, status=status.HTTP_200_OK)
