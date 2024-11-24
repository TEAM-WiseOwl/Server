from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import College, ExceptionDepartmentSubject, ExceptionGenedSubject, ExtraForeignTest, ForeignTestRequired, GeneralSubjectCompleted, MajorSubjectCompleted, OpeningSemester, Department, GenedCategory, RequiredCredit, Requirement, SubjectDepartment, SubjectDepartmentRequired, SubjectGened, SubjectGenedRequired
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
        major_requirements = Requirement.objects.filter(department=major_department, graduation_gubun="본전공").first()
        major_tests = ForeignTestRequired.objects.filter(department=major_department)
        major_extra_tests = ExtraForeignTest.objects.filter(department=major_department)

        graduation_gubun_value = None
        if graduation_gubun in ["전공심화+부전공", "부전공"]:
            graduation_gubun_value = "부전공"
        elif graduation_gubun == "이중전공":
            graduation_gubun_value = "이중전공"

        # 이중/부전공 데이터
        double_minor_requirements = Requirement.objects.filter(department=double_minor_department, graduation_gubun=graduation_gubun_value).first() if double_minor_department else None
        double_minor_tests = ForeignTestRequired.objects.filter(department=double_minor_department) if double_minor_department else None
        double_minor_extra_tests = ExtraForeignTest.objects.filter(department=double_minor_department) if double_minor_department else None

        # 응답 데이터 구조 생성
        result = {
            "major": {
                "requirement_description": major_requirements.description if major_requirements else None,
                "extra_foreign_test": [
                    {
                        "description": test.description,
                        "extra_test_name": test.extra_test_name,
                        "extra_test_basic_score": test.extra_test_basic_score,
                    }
                    for test in major_extra_tests
                ] if major_extra_tests.exists() else None,  # 없으면 null
                "lang_test": {
                    "basic": [],
                    "etc": []
                }
            },
            "double_or_minor": {
                "requirement_description": double_minor_requirements.description if double_minor_requirements else None,
                "extra_foreign_test": [
                    {
                        "description": test.description,
                        "extra_test_name": test.extra_test_name,
                        "extra_test_basic_score": test.extra_test_basic_score,
                    }
                    for test in double_minor_extra_tests
                ] if double_minor_extra_tests and double_minor_extra_tests.exists() else None,  # 없으면 null
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

class GraduationGraphAPIView(APIView):
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
        lower_bound, upper_bound = GraduationGraphAPIView.parse_required_credit_sn(required_credit_sn)
        if lower_bound is not None:
            if upper_bound is not None:
                return lower_bound <= student_number <= upper_bound
            return student_number >= lower_bound
        return False

    def is_course_completed(self, required_code, user_courses, exception_table, course_type="major"):
        # 직접 매칭
        if course_type == "major":
            if required_code[:6] in {course.subject_department.subject_department_code[:6] for course in user_courses}:
                return True
        elif course_type == "gened":
            if required_code[:6] in {course.subject_gened.subject_gened_code[:6] for course in user_courses}:
                return True

        # 예외 처리 테이블 확인
        exceptions = exception_table.filter(comparison_code=required_code)
        for exception in exceptions:
            if exception.code_match:
                if course_type == "major":
                    if any(exception.comparison_code[:6] == course.subject_department.subject_department_code[:6] for course in user_courses):
                        return True
                elif course_type == "gened":
                    if any(exception.comparison_code[:6] == course.subject_gened.subject_gened_code[:6] for course in user_courses):
                        return True
            elif exception.name_match:
                if course_type == "major":
                    if any(exception.comparison_name == course.subject_department.subject_department_name for course in user_courses):
                        return True
                elif course_type == "gened":
                    if any(exception.comparison_name == course.subject_gened.subject_gened_name for course in user_courses):
                        return True
        return False

    def update_graduation_status(self, profile, user_major_courses, user_gened_courses):
        major_department = profile.major
        major_required_courses = SubjectDepartmentRequired.objects.filter(department=major_department)
        liberal_required_courses = SubjectGenedRequired.objects.filter(department=major_department)

        major_required_completed = all(
            self.is_course_completed(
                required.subject_department_required_code,
                user_major_courses,
                ExceptionDepartmentSubject.objects.filter(department=major_department),
                course_type="major"
            )
            for required in major_required_courses
        )

        liberal_required_completed = all(
            self.is_course_completed(
                required.subject_gened_required_code,
                user_gened_courses,
                ExceptionGenedSubject.objects.filter(department=major_department),
                course_type="gened"
            )
            for required in liberal_required_courses
        )

        profile.grad_required_completed = major_required_completed and liberal_required_completed
        profile.save()

    def get(self, request):
        user = request.user

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        user_major_courses = MajorSubjectCompleted.objects.filter(user=user)
        user_gened_courses = GeneralSubjectCompleted.objects.filter(user=user)

        self.update_graduation_status(profile, user_major_courses, user_gened_courses)

        result = {
            "main_major_completion_rate": None,
            "double_major_completion_rate": None,
            "liberal_completion_rate": None,
            "completed_credits": [
                {
                    "main_major_credits": 0,
                    "double_minor_major_credits": 0,
                    "liberal_credits": 0,
                    "elective_credits": 0,
                }
            ],
            "required_credits": [
                {
                    "main_major_graduation_credits": None,
                    "double_minor_major_graduation_credits": None,
                    "liberal_graduation_credits": None,
                }
            ]
        }

        # 졸업 요건 데이터 가져오기
        required_credits = RequiredCredit.objects.filter(
            college=profile.major_college,
            required_credit_gubun=profile.profile_gubun
        ).first()

        if required_credits:
            result["required_credits"][0]["main_major_graduation_credits"] = required_credits.required_major_credit
            result["required_credits"][0]["double_minor_major_graduation_credits"] = required_credits.required_double_or_minor_credit
            result["required_credits"][0]["liberal_graduation_credits"] = required_credits.required_gened_credit

        # 본전공 이수 학점 계산
        main_major_credits = sum(
            course.subject_department.subject_department_credit for course in user_major_courses
            if course.subject_department.department == profile.major
        )
        result["completed_credits"][0]["main_major_credits"] = main_major_credits

        # 이중/부전공 이수 학점 계산
        double_minor_major_credits = 0
        if profile.double_or_minor:
            double_minor_major_credits = sum(
                course.subject_department.subject_department_credit for course in user_major_courses
                if course.subject_department.department == profile.double_or_minor or
                   self.is_course_completed(
                       required_code=course.subject_department.subject_department_code,
                       user_courses=user_major_courses,
                       exception_table=ExceptionDepartmentSubject.objects.filter(department=profile.double_or_minor),
                       course_type="major"
                   )
            )
        result["completed_credits"][0]["double_minor_major_credits"] = double_minor_major_credits

        # 교양 이수 학점 계산
        liberal_credits = sum(
            course.subject_gened.subject_gened_credit for course in user_gened_courses
        )
        result["completed_credits"][0]["liberal_credits"] = liberal_credits

        # 자선 학점 계산
        if result["required_credits"][0]["liberal_graduation_credits"]:
            liberal_required = result["required_credits"][0]["liberal_graduation_credits"]
            if liberal_credits > liberal_required:
                result["completed_credits"][0]["elective_credits"] += liberal_credits - liberal_required

        if result["required_credits"][0]["main_major_graduation_credits"]:
            main_major_required = result["required_credits"][0]["main_major_graduation_credits"]
            if main_major_credits > main_major_required:
                result["completed_credits"][0]["elective_credits"] += main_major_credits - main_major_required

        if profile.double_or_minor and result["required_credits"][0]["double_minor_major_graduation_credits"]:
            double_minor_required = result["required_credits"][0]["double_minor_major_graduation_credits"]
            if double_minor_major_credits > double_minor_required:
                result["completed_credits"][0]["elective_credits"] += double_minor_major_credits - double_minor_required

        # 완료율 계산
        if result["required_credits"][0]["main_major_graduation_credits"]:
            result["main_major_completion_rate"] = round(
                (main_major_credits / result["required_credits"][0]["main_major_graduation_credits"]) * 100, 1
            )

        if profile.double_or_minor and result["required_credits"][0]["double_minor_major_graduation_credits"]:
            result["double_major_completion_rate"] = round(
                (double_minor_major_credits / result["required_credits"][0]["double_minor_major_graduation_credits"]) * 100, 1
            )

        if result["required_credits"][0]["liberal_graduation_credits"]:
            result["liberal_completion_rate"] = round(
                (liberal_credits / result["required_credits"][0]["liberal_graduation_credits"]) * 100, 1
            )

        return Response(result, status=status.HTTP_200_OK)

class RequirementAPIView(APIView):
    def get(self, request):
        user = request.user
        
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 사용자 기본 정보
        major_department = profile.major
        double_minor_department = profile.double_or_minor
        graduation_gubun = profile.profile_gubun

        # Helper 함수: 이수 여부 확인
        def is_course_completed(required_code, user_courses, exception_table):
            if required_code[:6] in {course.subject_department.subject_department_code[:6] for course in user_courses}:
                return True

            exceptions = exception_table.filter(subject_department_required_code=required_code)
            for exception in exceptions:
                if exception.code_match:
                    if any(exception.comparison_code[:6] == course.subject_department.subject_department_code[:6] for course in user_courses):
                        return True
                elif exception.name_match:
                    if any(exception.comparison_name == course.subject_department.subject_department_name for course in user_courses):
                        return True

            return False

        # 사용자 전공 이수 학점
        user_major_courses = MajorSubjectCompleted.objects.filter(
            user=user,
            subject_department__department=major_department
        )
        major_credit_completed = sum(
            course.subject_department.subject_department_credit for course in user_major_courses
        )

        # 본전공 필수 과목 이수 확인
        major_required_courses = SubjectDepartmentRequired.objects.filter(department=major_department)
        major_required_completed = all(
            is_course_completed(
                required.subject_department_required_code,
                user_major_courses,
                ExceptionDepartmentSubject.objects.filter(department=major_department)
            )
            for required in major_required_courses
        )

        grad_requirments = major_credit_completed >= 100 and major_required_completed

        # 이중/부전공 이수 학점 및 필수 과목 확인
        double_credit_completed = 0
        double_grad_requirments = False

        if double_minor_department:
            user_double_minor_courses = MajorSubjectCompleted.objects.filter(
                user=user,
                subject_department__department=double_minor_department
            )
            double_credit_completed = sum(
                course.subject_department.subject_department_credit for course in user_double_minor_courses
            )

            # 이중/부전공 필수 과목 확인
            double_required_courses = SubjectDepartmentRequired.objects.filter(department=double_minor_department)
            double_required_completed = all(
                is_course_completed(
                    required.subject_department_required_code,
                    user_double_minor_courses,
                    ExceptionDepartmentSubject.objects.filter(department=double_minor_department)
                )
                for required in double_required_courses
            )

            double_grad_requirments = double_credit_completed >= 50 and double_required_completed

        # 졸업 요구사항 반환
        result = {
            "main_major_conditions": {
                "complete_requirment": [
                    {
                        "grad_research": profile.grad_research,
                        "grad_exam": profile.grad_exam,
                        "grad_pro": profile.grad_pro,
                        "grad_certificate": profile.grad_certificate,
                        "for_langauge": profile.for_language,
                        "grad_requirments": grad_requirments
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
                        "double_for_langauge": profile.double_for_language,
                        "double_grad_requirments": double_grad_requirments
                    }
                ]
            }
        }

        return Response(result, status=status.HTTP_200_OK)

class RequirementSubjectAPIView(APIView):
    def get(self, request):
        user = request.user

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        # 사용자 정보 가져오기
        major_department = profile.major
        double_minor_department = profile.double_or_minor

        # Helper 함수: 이수 여부 확인
        def is_course_completed(required_code, user_courses, exception_table, course_type="major"):
            if course_type == "major":
                if required_code[:6] in {course.subject_department.subject_department_code[:6] for course in user_courses}:
                    return True
            elif course_type == "gened":
                if required_code[:6] in {course.subject_gened.subject_gened_code[:6] for course in user_courses}:
                    return True

            exceptions = exception_table.filter(comparison_code=required_code)
            for exception in exceptions:
                if exception.code_match:
                    if course_type == "major":
                        if any(exception.comparison_code[:6] == course.subject_department.subject_department_code[:6] for course in user_courses):
                            return True
                    elif course_type == "gened":
                        if any(exception.comparison_code[:6] == course.subject_gened.subject_gened_code[:6] for course in user_courses):
                            return True
                elif exception.name_match:
                    if course_type == "major":
                        if any(exception.comparison_name == course.subject_department.subject_department_name for course in user_courses):
                            return True
                    elif course_type == "gened":
                        if any(exception.comparison_name == course.subject_gened.subject_gened_name for course in user_courses):
                            return True
            return False

        # 사용자 주전공 과목 가져오기
        user_major_courses = MajorSubjectCompleted.objects.filter(
            user=user,
            subject_department__department=major_department
        )

        # 사용자 복수전공/부전공 과목 가져오기
        user_double_minor_courses = MajorSubjectCompleted.objects.filter(
            user=user,
            subject_department__department=double_minor_department
        )

        # 교양 과목 가져오기
        user_gened_courses = GeneralSubjectCompleted.objects.filter(user=user)

        # 주전공 필수 과목
        main_major_required_courses = []
        required_courses = SubjectDepartmentRequired.objects.filter(
            department=major_department,
            subject_department_required_1=True
        )

        for required_course in required_courses:
            completion_status = is_course_completed(
                required_course.subject_department_required_code,
                user_major_courses,
                ExceptionDepartmentSubject.objects.filter(department=major_department),
                course_type="major"
            )
            main_major_required_courses.append({
                "completion_status": completion_status,
                "subject_department_name": required_course.subject_department_required_name,
                "subject_department_code": required_course.subject_department_required_code
            })

        # 복수전공/부전공 필수 과목
        double_minor_required_courses = []
        if double_minor_department:
            required_courses = SubjectDepartmentRequired.objects.filter(
                department=double_minor_department,
                subject_department_required_2=True
            )

            for required_course in required_courses:
                completion_status = is_course_completed(
                    required_course.subject_department_required_code,
                    user_double_minor_courses,
                    ExceptionDepartmentSubject.objects.filter(department=double_minor_department),
                    course_type="major"
                )
                double_minor_required_courses.append({
                    "completion_status": completion_status,
                    "subject_department_name": required_course.subject_department_required_name,
                    "subject_department_code": required_course.subject_department_required_code
                })

        # 교양 필수 과목
        liberal_required_courses = []
        for required_course in SubjectGenedRequired.objects.filter(department=major_department):
            completion_status = is_course_completed(
                required_course.subject_gened_required_code,
                user_gened_courses,
                ExceptionGenedSubject.objects.filter(department=major_department),
                course_type="gened"
            )

            # 교양 과목 정보 가져오기
            linked_subject = SubjectGened.objects.filter(subject_gened_code__startswith=required_course.subject_gened_required_code[:6]).first()
            liberal_required_courses.append({
                "completion_status": completion_status,
                "subject_gened_code": required_course.subject_gened_required_code,
                "gen_category_name": linked_subject.gened_category.gened_category_name if linked_subject else None,
                "subject_gened_name": linked_subject.subject_gened_name if linked_subject else None
            })

        # 응답 데이터 생성
        response_data = {
            "main_major": [
                {
                    "major_id": major_department.department_id,
                    "department_name": major_department.department_name
                }
            ],
            "double_major": [
                {
                    "double_or_minor_id": double_minor_department.department_id if double_minor_department else None,
                    "department_name": double_minor_department.department_name if double_minor_department else None
                }
            ],
            "main_major_required_courses": main_major_required_courses,
            "double_or_minor_required_courses": double_minor_required_courses,
            "liberal_required_courses": liberal_required_courses,
        }

        return Response(response_data, status=status.HTTP_200_OK)
