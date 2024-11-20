from django.db import models
from django.conf import settings
# Create your models here.
class College(models.Model):
    college_id=models.BigAutoField(verbose_name="단과대 아이디", primary_key=True)
    college_name=models.CharField(verbose_name="단과대명", max_length=30)
    college_required_credit=models.IntegerField(verbose_name="졸업이수학점", null=True)

class Department(models.Model):
    department_id=models.BigAutoField(verbose_name="학과 아이디", primary_key=True)
    college=models.ForeignKey(College, on_delete=models.CASCADE)
    department_name=models.CharField(verbose_name="학과 이름", max_length=50)
    department_url=models.URLField(verbose_name="학과페이지 url", max_length=200)

class Requirement(models.Model):
    id= models.BigAutoField(verbose_name="졸업 요건 id", primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    graduation_thesis=models.BooleanField(verbose_name="졸논 필요 여부", default = False)
    graduation_exam=models.BooleanField(verbose_name="졸업시험 필요 여부", default = False)
    graduation_project=models.BooleanField(verbose_name="졸플 필요 여부", default = False)
    graduation_qualifications=models.BooleanField(verbose_name="자격증 필요 여부", default = False)
    graduation_subjects=models.BooleanField(verbose_name="졸업 필요 여부", default = False)
    graduation_gubun=models.CharField(verbose_name="이중전공,부전공,전공심화", max_length=20, null=True)
    description=models.CharField(verbose_name="기타사항(예를 들면 시험 대체가능)", max_length=500, null=True)

class OpeningSemester(models.Model):
    opening_semester_id=models.BigAutoField(verbose_name="개설학기 아이디", primary_key=True)
    subject_semester=models.CharField(verbose_name="개설학기", max_length=10)
    
class GenedCategory(models.Model):
    gened_category_id=models.BigAutoField(verbose_name="교양 카테고리 아이디", primary_key=True)
    gened_category_name=models.CharField(verbose_name="교양 카테고리 이름", max_length=20)

class SubjectGened(models.Model):
    subject_gened_id = models.BigAutoField(verbose_name="교양과목 아이디", primary_key=True)
    gened_category = models.ForeignKey(GenedCategory, on_delete=models.CASCADE, null=False)
    subject_gened_code=models.CharField(verbose_name="교양 과목코드", max_length=50)
    subject_gened_name=models.CharField(verbose_name="교양 과목명", max_length=150)
    subject_gened_credit=models.IntegerField(verbose_name="교양과목 학점")
    subject_gened_professor=models.CharField(verbose_name="교수명", max_length=100)
    subject_gened_room_date=models.CharField(verbose_name="강의시간/강의실", max_length=50, null=True)
    opening_semester=models.ForeignKey(OpeningSemester, on_delete=models.CASCADE, null=False)

class SubjectGenedRequired(models.Model): 
    subject_gened_required_code=models.CharField(verbose_name="교양 필수 과목코드", max_length=50, null=True)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_gened_required_db=models.BooleanField(verbose_name="이중전공 여부", default = False)
    subject_gened_required_sn=models.CharField(verbose_name="학번(이상)", max_length=30)
    subject_gened_required_name = models.CharField(verbose_name="교양필수 과목명", max_length = 150, null = True)
    subject_gened_required_desc = models.CharField(verbose_name = "설명", max_length = 500 , null = True)
    subject_gened_required_instead = models.BooleanField(verbose_name="대체 가능 여부", default = False)

    class Meta:
        unique_together = ('subject_gened_required_code', 'department')  # Django 2.2 이전 버전에서 사용 가능
        # Django 2.2 이상 버전에서는 아래와 같이 UniqueConstraint를 사용할 수도 있음
        # constraints = [
        #     models.UniqueConstraint(fields=['subject_gened_id', 'department_id'], name='subject_gened_id_department_id')
        # ]

class SubjectDepartment(models.Model):
    subject_department_id=models.BigAutoField(verbose_name="전공과목 아이디", primary_key=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_department_code=models.CharField(verbose_name="전공 과목코드", max_length=50)
    subject_department_name=models.CharField(verbose_name="전공 과목명", max_length=150)
    subject_department_credit=models.IntegerField(verbose_name="전공과목 학점")
    subject_department_professor=models.CharField(verbose_name="교수명", max_length=100)
    subject_department_room_date=models.CharField(verbose_name="강의시간/강의실", max_length=50, null=True)
    opening_semester=models.ForeignKey(OpeningSemester, on_delete=models.CASCADE, null=False)

class SubjectDepartmentRequired(models.Model):
    subject_department_required_id = models.BigAutoField(verbose_name="전공필수과목 아이디", primary_key=True, default=0)
    subject_department_required_code=models.CharField( verbose_name="전공 필수 과목코드", max_length=50, null = True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_department_required_1=models.BooleanField(verbose_name="본전공만만 해당 여부", default = False)
    subject_department_required_2=models.BooleanField(verbose_name="이중전공만 해당 여부", default = False)
    subject_department_required_sn=models.CharField(verbose_name="학번(이상)", max_length=30)
    subject_department_required_name = models.CharField(verbose_name="전공필수 과목명", max_length = 150, null=True)
    subject_department_required_desc = models.CharField(verbose_name = "설명", max_length = 500, null = True)
    subject_department_required_instead = models.BooleanField(verbose_name="대체 가능 여부", default = False)



class GeneralSubjectCompleted(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_gened=models.ForeignKey(SubjectGened, on_delete=models.CASCADE)
    grade=models.CharField(verbose_name="성적", max_length=5)
    retry_yn=models.BooleanField(verbose_name="재수강 여부", default = False)
    school_year=models.IntegerField(verbose_name="학년/학기")
    completed_year=models.CharField(verbose_name="수강년도", max_length=5)

    class Meta:
        unique_together = ('user', 'subject_gened')  # Django 2.2 이전 버전에서 사용 가능
        # Django 2.2 이상 버전에서는 아래와 같이 UniqueConstraint를 사용할 수도 있음
        # constraints = [
        #     models.UniqueConstraint(fields=['subject_gened_id', 'department_id'], name='subject_gened_id_department_id')
        # ]

class MajorSubjectCompleted(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_department=models.ForeignKey(SubjectDepartment, on_delete=models.CASCADE)
    grade=models.CharField(verbose_name="성적", max_length=5, default='A+')
    retry_yn=models.BooleanField(verbose_name="재수강 여부", default = False)
    school_year=models.IntegerField(verbose_name="학년/학기")
    completed_year=models.CharField(verbose_name="수강년도", max_length=10)

    class Meta:
        unique_together = ('user', 'subject_department')  # Django 2.2 이전 버전에서 사용 가능
        # Django 2.2 이상 버전에서는 아래와 같이 UniqueConstraint를 사용할 수도 있음
        # constraints = [
        #     models.UniqueConstraint(fields=['subject_gened_id', 'department_id'], name='subject_gened_id_department_id')
        # ] 

class ForeignTestRequired(models.Model):
    test_id=models.BigAutoField(verbose_name="시험 아이디", primary_key=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    test_name=models.CharField(verbose_name="시험명", max_length=15)
    test_basic_score=models.CharField(verbose_name="요건 통과 기준 점수", max_length=20, null=True)

class RequiredCredit(models.Model):
    required_credit_id=models.BigAutoField(verbose_name="졸업이수학점 아이디", primary_key=True)
    college=models.ForeignKey(College, on_delete=models.CASCADE)
    required_credit_sn=models.CharField(verbose_name="학번(이상)", max_length=50)
    required_credit_gubun=models.CharField(verbose_name="이수구분(이중,부전,전공심화", max_length=10)
    required_major_credit=models.IntegerField(verbose_name="전공이수필요학점")
    required_double_or_minor_credit=models.IntegerField(verbose_name="이중(부)전공이수필요학점")
    required_gened_credit=models.IntegerField(verbose_name="교양이수필요학점")

class ExtraForeignTest(models.Model):
    extra_test_id=models.BigAutoField(verbose_name="기타시험 아이디", primary_key=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    extra_test_name=models.CharField(verbose_name="기타시험 이름", max_length=30)
    extra_test_basic_score=models.CharField(verbose_name="기준", max_length=20, null=True)
    extra_test_gubun=models.CharField(verbose_name="졸시/자격증", max_length=20)
    description=models.CharField(verbose_name="추가정보/예를 들면 이중만 조건 다른 경우", max_length=200, null=True)

class ExceptionDepartmentSubject(models.Model):
    subject_department_required_code = models.CharField(verbose_name="전공필수 과목코드", max_length=50, null=True)
    comparison_code = models.CharField(verbose_name="대체 과목코드", max_length=50)
    comparison_name = models.CharField(verbose_name="대체 과목명", max_length=150)
    code_match = models.BooleanField(verbose_name="코드값 일치", default = False)
    name_match = models.BooleanField(verbose_name="과목명 일치", default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default = 0)

    class Meta:
        unique_together = ('subject_department_required_code', 'comparison_code')

class ExceptionGenedSubject(models.Model):
    subject_gened_required_code = models.CharField(verbose_name="교양필수 과목코드", max_length=50, null=True)
    comparison_code = models.CharField(verbose_name="대체 과목코드", max_length=50)
    comparison_name = models.CharField(verbose_name="대체 과목명", max_length=150)
    code_match = models.BooleanField(verbose_name="코드값 일치", default = False)
    name_match = models.BooleanField(verbose_name="과목명 일치", default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=0)

    class Meta:
        unique_together = ('subject_gened_required_code', 'comparison_code', 'department')