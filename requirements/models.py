from django.db import models
from django.conf import settings
# Create your models here.
class College(models.Model):
    college_id=models.BigAutoField(verbose_name="단과대 아이디", primary_key=True)
    college_name=models.CharField(verbose_name="단과대명", max_length=30)
    college_required_credit=models.IntegerField(verbose_name="졸업이수학점")
class Department(models.Model):
    department_id=models.BigAutoField(verbose_name="학과 아이디", primary_key=True)
    college_id=models.ForeignKey(College, on_delete=models.CASCADE)
    department_name=models.CharField(verbose_name="학과 이름", max_length=50)
    department_url=models.URLField(verbose_name="학과페이지 url", max_length=200)
class Requirement(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, primary_key=True)
    graduation_thesis=models.BooleanField(verbose_name="졸논 필요 여부", default = False)
    graduation_exam=models.BooleanField(verbose_name="졸업시험 필요 여부", default = False)
    graduation_project=models.BooleanField(verbose_name="졸플 필요 여부", default = False)
    graduation_qualifications=models.BooleanField(verbose_name="자격증 필요 여부", default = False)
    graduation_subjects=models.BooleanField(verbose_name="졸업 필요 여부", default = False)

class Opening_semester(models.required):
    opening_semester_id=models.BigAutoField(verbose_name="개설학기 아이디", primary_key=True)
    suject_year=models.CharField(verbose_name="개설년도", max_length=7)
    suject_year=models.CharField(verbose_name="개설학기", max_length=7)
    
class Gened_category(models.Model):
    gened_category_id=models.BigAutoField(verbose_name="교양 카테고리 아이디", primary_key=True)
    gened_category_name=models.CharField(verbose_name="교양 카테고리 이름", max_length=20)

class Subject_gened(models.Model):
    subject_gened_id = models.BigAutoField(verbose_name="교양과목 아이디", primary_key=True)
    gened_category_id = models.ForeignKey(Gened_category, on_delete=models.CASCADE, null=False)
    subject_gened_code=models.CharField(verbose_name="교양 과목코드", max_length=50)
    subject_gened_name=models.CharField(verbose_name="교양 과목명", max_length=50)
    subject_gened_credit=models.IntegerField(verbose_name="교양과목 학점")
    subject_gened_professor=models.CharField(verbose_name="교수명", max_length=30)
    subject_gened_room=models.CharField(verbose_name="강의실", max_length=10)
    subject_gened_date=models.CharField(verbose_name="강의시간", max_length=14)
    subject_gened_date=models.CharField(verbose_name="강의시간", max_length=14)
    opening_semester_id=models.ForeignKey(Opening_semester, on_delete=models.CASCADE, null=False)

class Subject_gened_required(models.Model):
    subject_gened_id=models.ForeignKey(Subject_gened, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_gened_required_db=models.BooleanField(verbose_name="이중전공 여부", default = False)
    subject_gened_required_sn=models.IntegerField(verbose_name="학번(이상)")

    class Meta:
        unique_together = ('subject_gened_id', 'department_id')  # Django 2.2 이전 버전에서 사용 가능
        # Django 2.2 이상 버전에서는 아래와 같이 UniqueConstraint를 사용할 수도 있음
        # constraints = [
        #     models.UniqueConstraint(fields=['subject_gened_id', 'department_id'], name='subject_gened_id_department_id')
        # ]

class Subject_department(models.Model):
    subject_department_id=models.BigAutoField(verbose_name="전공과목 아이디", primary_key=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_department_code=models.CharField(verbose_name="전공 과목코드", max_length=50)
    subject_department_name=models.CharField(verbose_name="전공 과목명", max_length=50)
    subject_department_credit=models.IntegerField(verbose_name="전공과목 학점")
    subject_department_professor=models.CharField(verbose_name="교수명", max_length=30)
    subject_department_room=models.CharField(verbose_name="강의실", max_length=10)
    subject_department_date=models.CharField(verbose_name="강의시간", max_length=14)
    opening_semester_id=models.ForeignKey(Opening_semester, on_delete=models.CASCADE, null=False)

class Subject_department_required(models.Model):
    subject_requirement_id=models.ForeignKey(Subject_department, on_delete=models.CASCADE)
    department_id=models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_gened_required_db=models.BooleanField(verbose_name="이중전공 여부", default = False)
    subject_gened_required_sn=models.IntegerField(verbose_name="학번(이상)")

    class Meta:
        unique_together = ('subject_requirement_id', 'department_id')  # Django 2.2 이전 버전에서 사용 가능
        # Django 2.2 이상 버전에서는 아래와 같이 UniqueConstraint를 사용할 수도 있음
        # constraints = [
        #     models.UniqueConstraint(fields=['subject_gened_id', 'department_id'], name='subject_gened_id_department_id')
        # ]


class General_subject_completed(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_gened_id=models.ForeignKey(Subject_gened, on_delete=models.CASCADE, null=False)
    grade=models.CharField(verbose_name="성적", max_length=5)
    retry_yn=models.BooleanField(verbose_name="재수강 여부", default = False)
    school_year=models.IntegerField(verbose_name="학년/학기")
    completed_year=models.CharField(verbose_name="수강년도", max_length=5)
    class Meta:
        unique_together = ('user_id', 'subject_gened_id')  # Django 2.2 이전 버전에서 사용 가능
        # Django 2.2 이상 버전에서는 아래와 같이 UniqueConstraint를 사용할 수도 있음
        # constraints = [
        #     models.UniqueConstraint(fields=['subject_gened_id', 'department_id'], name='subject_gened_id_department_id')
        # ]

class major_subject_completed(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_department_id=models.ForeignKey(Subject_department, on_delete=models.CASCADE, null=False)
    grade=models.CharField(verbose_name="성적", max_length=5)
    retry_yn=models.BooleanField(verbose_name="재수강 여부", default = False)
    school_year=models.IntegerField(verbose_name="학년/학기")
    completed_year=models.CharField(verbose_name="수강년도", max_length=5)
    class Meta:
        unique_together = ('user_id', 'subject_department_id')  # Django 2.2 이전 버전에서 사용 가능
        # Django 2.2 이상 버전에서는 아래와 같이 UniqueConstraint를 사용할 수도 있음
        # constraints = [
        #     models.UniqueConstraint(fields=['subject_gened_id', 'department_id'], name='subject_gened_id_department_id')
        # ] 
class Foreign_test_required(models.Model):
    test_id=models.BigAutoField(verbose_name="시험 아이디", primary_key=True)
    department_id=models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    test_name=models.CharField(verbose_name="시험명", max_length=15)
    test_basic_score=models.IntegerField(verbose_name="요건 통과 기준 점수")

class Required_credit(models.Model):
    required_credit_id=models.BigAutoField(verbose_name="졸업이수학점 아이디", primary_key=True)
    college_id=models.ForeignKey(College, on_delete=models.CASCADE)
    required_credit_sn=models.IntegerField(verbose_name="학번(이상)")
    required_credit_gubun=models.CharField(verbose_name="이수구분(이중,부전,전공심화", max_length=10)
    required_major_credit=models.IntegerField(verbose_name="전공이수필요학점")
    required_double_or_minor_credit=models.IntegerField(verbose_name="이중(부)전공이수필요학점")
    required_gened_credit=models.IntegerField(verbose_name="교양이수필요학점")

