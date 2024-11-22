from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sympy import Sum
from .models import College, ForeignTestRequired, GeneralSubjectCompleted, MajorSubjectCompleted, OpeningSemester, Department, GenedCategory, RequiredCredit, Requirement, SubjectDepartment, SubjectGened
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
        graduation_gubun = profile.profile_gubun
        
        # 본전공 데이터
        major_requirements = Requirement.objects.filter(department=major_department, graduation_gubun = "본전공").first()
        major_tests = ForeignTestRequired.objects.filter(department=major_department)

        graduation_gubun_value = None

        if graduation_gubun in ["전공심화+부전공", "부전공"]:
            graduation_gubun_value = "부전공"
        elif graduation_gubun == "이중전공":
            graduation_gubun_value = "이중전공"

        # 이중/부전공 데이터
        double_minor_requirements = Requirement.objects.filter(department=double_minor_department, graduation_gubun = graduation_gubun_value).first() if double_minor_department else None
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

class GraduationProgressAPIView(APIView):
    @staticmethod
    def parse_required_credit_sn(required_credit_sn):
        if "~" in required_credit_sn:
            parts = required_credit_sn.split("~")
            lower_bound = int(parts[0])
            upper_bound = int(parts[1]) if len(parts) > 1 and parts[1] else None
            return lower_bound, upper_bound
        return None, None

    @staticmethod
    def is_in_credit_sn_range(required_credit_sn, student_number):
        lower_bound, upper_bound = GraduationProgressAPIView.parse_required_credit_sn(required_credit_sn)
        if lower_bound is not None:
            if upper_bound is not None:
                return lower_bound <= student_number <= upper_bound
            return student_number >= lower_bound
        return False

    def get(self, request):
        user = request.user.user_id

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        result = {
            "main_major_completion_rate": None,
            "double_major_completion_rate": None,
            "liberal_completion_rate": None,
            "completed_credits": {
                "main_major_credits": None,
                "double_minor_major_credits": None,
                "liberal_credits": None,
                "elective_credits": 0,
            },
            "required_credits": {
                "main_major_graduation_credits": None,
                "double_minor_major_graduation_credits": None,
                "liberal_graduation_credits": None,
            },
        }

        required_credits_all = RequiredCredit.objects.filter(
            college=profile.major_college,
            required_credit_gubun=profile.profile_gubun,
        )

        required_credits = None
        for credit in required_credits_all:
            if credit.required_credit_sn.isdigit() or "~" in credit.required_credit_sn:
                if self.is_in_credit_sn_range(credit.required_credit_sn, profile.profile_student_number):
                    required_credits = credit
                    break
            else:
                if credit.required_credit_sn == profile.major.department_name:
                    required_credits = credit
                    break
                if credit.required_credit_sn == "C&T" and profile.major.department_name in ["디지털콘텐츠학부", "투어리즘 & 웰니스학부"]:
                    required_credits = credit
                    break
                if credit.required_credit_sn == "글로벌스포츠산업학부" and profile.major.department_name == "글로벌스포츠산업학부":
                    required_credits = credit
                    break

        if required_credits:
            result["required_credits"]["main_major_graduation_credits"] = required_credits.required_major_credit
            result["required_credits"]["double_minor_major_graduation_credits"] = required_credits.required_double_or_minor_credit
            result["required_credits"]["liberal_graduation_credits"] = required_credits.required_gened_credit

        main_major_queryset = MajorSubjectCompleted.objects.filter(user=user, subject_department__department=profile.major)
        main_major_credits = sum(
            record.subject_department.subject_department_credit for record in main_major_queryset
        )
        result["completed_credits"]["main_major_credits"] = main_major_credits

        double_minor_major_credits = 0
        if profile.double_or_minor:
            double_major_queryset = MajorSubjectCompleted.objects.filter(
                user=user, subject_department__department=profile.double_or_minor
            )
            double_minor_major_credits = sum(
                record.subject_department.subject_department_credit for record in double_major_queryset
            )
        result["completed_credits"]["double_minor_major_credits"] = double_minor_major_credits

        liberal_queryset = GeneralSubjectCompleted.objects.filter(
            user=user, subject_gened__subject_gened_credit__isnull=False
        )
        liberal_credits = sum(
            record.subject_gened.subject_gened_credit for record in liberal_queryset
        )
        result["completed_credits"]["liberal_credits"] = liberal_credits

        if result["required_credits"]["liberal_graduation_credits"]:
            liberal_required = result["required_credits"]["liberal_graduation_credits"]
            if liberal_credits > liberal_required:
                result["completed_credits"]["elective_credits"] += liberal_credits - liberal_required

        if result["required_credits"]["main_major_graduation_credits"]:
            main_major_required = result["required_credits"]["main_major_graduation_credits"]
            if main_major_credits > main_major_required:
                result["completed_credits"]["elective_credits"] += main_major_credits - main_major_required

        if profile.double_or_minor and result["required_credits"]["double_minor_major_graduation_credits"]:
            double_minor_required = result["required_credits"]["double_minor_major_graduation_credits"]
            if double_minor_major_credits > double_minor_required:
                result["completed_credits"]["elective_credits"] += double_minor_major_credits - double_minor_required

        if result["required_credits"]["main_major_graduation_credits"]:
            result["main_major_completion_rate"] = round(
                (main_major_credits / result["required_credits"]["main_major_graduation_credits"]) * 100, 1
            )

        if profile.double_or_minor and result["required_credits"]["double_minor_major_graduation_credits"]:
            result["double_major_completion_rate"] = round(
                (double_minor_major_credits / result["required_credits"]["double_minor_major_graduation_credits"]) * 100, 1
            )

        if result["required_credits"]["liberal_graduation_credits"]:
            result["liberal_completion_rate"] = round(
                (liberal_credits / result["required_credits"]["liberal_graduation_credits"]) * 100, 1
            )

        return Response(result, status=status.HTTP_200_OK)

class RequirementAPIView(APIView):
    def get(self, request):
        user = request.user
        
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        major_department = profile.major
        double_minor_department = profile.double_or_minor
        graduation_gubun = profile.profile_gubun

        major_requirements = Requirement.objects.filter(department=major_department, graduation_gubun = "본전공").first()
        major_tests = ForeignTestRequired.objects.filter(department=major_department).exists()
        
        graduation_gubun_value = None
        
        if graduation_gubun in ["전공심화+부전공", "부전공"]:
            graduation_gubun_value = "부전공"
        elif graduation_gubun == "이중전공":
            graduation_gubun_value = "이중전공"

        double_minor_requirements = Requirement.objects.filter(department=double_minor_department, graduation_gubun = graduation_gubun_value).first() if double_minor_department else None
       
        result = {
            "main_major_conditions": {
                "complete_requirment": [
                {
                    "grad_research": profile.grad_research,
                    "grad_exam": profile.grad_exam,
                    "grad_pro": profile.grad_pro,
                    "grad_certificate": profile.grad_certificate,
                    "for_langauge": profile.for_language
                }
                ],
                "requirement": [
                {
                    "graduation_foreign": True if major_tests else False,
                    "graduation_project": major_requirements.graduation_project,
                    "graduation_exam": major_requirements.graduation_exam,
                    "graduation_thesis": major_requirements.graduation_thesis,
                    "graduation_qualifications": major_requirements.graduation_qualifications,
                    "graduation_requirments": major_requirements.graduation_subjects
                }
                ]
            },
            "double_minor_major_conditions": {
                "double_complete_requirment": [
                {
                    "double_grad_research": profile.double_grad_research,
                    "double_grad_exam": profile.double_grad_exam,
                    "double_grad_pro": profile.double_grad_pro,
                    "double_grad_certificate": profile.double_grad_certificate,
                    "double_for_langauge": profile.double_for_language
                }
                ],
                "requirement": [
                {
                    "graduation_project": double_minor_requirements.graduation_project,
                    "graduation_exam": double_minor_requirements.graduation_exam,
                    "graduation_thesis": double_minor_requirements.graduation_thesis,
                    "graduation_qualifications": double_minor_requirements.graduation_qualifications,
                    "graduation_requirments": double_minor_requirements.graduation_subjects
                }
                ]
            }
            }
        return Response(result, status=status.HTTP_200_OK)
