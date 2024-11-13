# Generated by Django 4.2 on 2024-11-13 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="College",
            fields=[
                (
                    "college_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="단과대 아이디"
                    ),
                ),
                ("college_name", models.CharField(max_length=30, verbose_name="단과대명")),
                (
                    "college_required_credit",
                    models.IntegerField(null=True, verbose_name="졸업이수학점"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "department_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="학과 아이디"
                    ),
                ),
                (
                    "department_name",
                    models.CharField(max_length=50, verbose_name="학과 이름"),
                ),
                ("department_url", models.URLField(verbose_name="학과페이지 url")),
                (
                    "college",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.college",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GenedCategory",
            fields=[
                (
                    "gened_category_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="교양 카테고리 아이디"
                    ),
                ),
                (
                    "gened_category_name",
                    models.CharField(max_length=20, verbose_name="교양 카테고리 이름"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OpeningSemester",
            fields=[
                (
                    "opening_semester_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="개설학기 아이디"
                    ),
                ),
                ("subject_year", models.CharField(max_length=7, verbose_name="개설년도")),
                (
                    "subject_semester",
                    models.CharField(max_length=7, verbose_name="개설학기"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubjectGenedRequired",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject_gened_required_code",
                    models.CharField(
                        max_length=50, null=True, verbose_name="교양 필수 과목코드"
                    ),
                ),
                (
                    "subject_gened_required_db",
                    models.BooleanField(default=False, verbose_name="이중전공 여부"),
                ),
                (
                    "subject_gened_required_sn",
                    models.CharField(max_length=30, verbose_name="학번(이상)"),
                ),
                (
                    "subject_gened_required_name",
                    models.CharField(max_length=20, null=True, verbose_name="교양필수 과목명"),
                ),
                (
                    "subject_gened_required_desc",
                    models.CharField(max_length=500, null=True, verbose_name="설명"),
                ),
                (
                    "subject_gened_required_instead",
                    models.BooleanField(default=False, verbose_name="대체 가능 여부"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
                (
                    "subject_gened_required_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.genedcategory",
                    ),
                ),
            ],
            options={
                "unique_together": {("subject_gened_required_code", "department")},
            },
        ),
        migrations.CreateModel(
            name="SubjectGened",
            fields=[
                (
                    "subject_gened_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="교양과목 아이디"
                    ),
                ),
                (
                    "subject_gened_code",
                    models.CharField(max_length=50, verbose_name="교양 과목코드"),
                ),
                (
                    "subject_gened_name",
                    models.CharField(max_length=50, verbose_name="교양 과목명"),
                ),
                ("subject_gened_credit", models.IntegerField(verbose_name="교양과목 학점")),
                (
                    "subject_gened_professor",
                    models.CharField(max_length=30, verbose_name="교수명"),
                ),
                (
                    "subject_gened_room_date",
                    models.CharField(max_length=50, null=True, verbose_name="강의시간/강의실"),
                ),
                (
                    "gened_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.genedcategory",
                    ),
                ),
                (
                    "opening_semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.openingsemester",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubjectDepartmentRequired",
            fields=[
                (
                    "subject_department_required_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="전공필수과목 아이디"
                    ),
                ),
                (
                    "subject_department_required_code",
                    models.CharField(
                        max_length=50, null=True, verbose_name="전공 필수 과목코드"
                    ),
                ),
                (
                    "subject_department_required_1",
                    models.BooleanField(default=False, verbose_name="본전공만만 해당 여부"),
                ),
                (
                    "subject_department_required_2",
                    models.BooleanField(default=False, verbose_name="이중전공만 해당 여부"),
                ),
                (
                    "subject_department_required_sn",
                    models.CharField(max_length=30, verbose_name="학번(이상)"),
                ),
                (
                    "subject_department_required_name",
                    models.CharField(max_length=20, null=True, verbose_name="전공필수 과목명"),
                ),
                (
                    "subject_department_required_desc",
                    models.CharField(max_length=500, null=True, verbose_name="설명"),
                ),
                (
                    "subject_department_required_instead",
                    models.BooleanField(default=False, verbose_name="대체 가능 여부"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubjectDepartment",
            fields=[
                (
                    "subject_department_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="전공과목 아이디"
                    ),
                ),
                (
                    "subject_department_code",
                    models.CharField(max_length=50, verbose_name="전공 과목코드"),
                ),
                (
                    "subject_department_name",
                    models.CharField(max_length=50, verbose_name="전공 과목명"),
                ),
                (
                    "subject_department_credit",
                    models.IntegerField(verbose_name="전공과목 학점"),
                ),
                (
                    "subject_department_professor",
                    models.CharField(max_length=30, verbose_name="교수명"),
                ),
                (
                    "subject_department_room_date",
                    models.CharField(max_length=50, null=True, verbose_name="강의시간/강의실"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
                (
                    "opening_semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.openingsemester",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Requirement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "graduation_thesis",
                    models.BooleanField(default=False, verbose_name="졸논 필요 여부"),
                ),
                (
                    "graduation_exam",
                    models.BooleanField(default=False, verbose_name="졸업시험 필요 여부"),
                ),
                (
                    "graduation_project",
                    models.BooleanField(default=False, verbose_name="졸플 필요 여부"),
                ),
                (
                    "graduation_qualifications",
                    models.BooleanField(default=False, verbose_name="자격증 필요 여부"),
                ),
                (
                    "graduation_subjects",
                    models.BooleanField(default=False, verbose_name="졸업 필요 여부"),
                ),
                (
                    "graduation_gubun",
                    models.CharField(
                        max_length=20, null=True, verbose_name="이중전공,부전공,전공심화"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500, null=True, verbose_name="기타사항(예를 들면 시험 대체가능)"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RequiredCredit",
            fields=[
                (
                    "required_credit_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="졸업이수학점 아이디"
                    ),
                ),
                (
                    "required_credit_sn",
                    models.CharField(max_length=50, verbose_name="학번(이상)"),
                ),
                (
                    "required_credit_gubun",
                    models.CharField(max_length=10, verbose_name="이수구분(이중,부전,전공심화"),
                ),
                ("required_major_credit", models.IntegerField(verbose_name="전공이수필요학점")),
                (
                    "required_double_or_minor_credit",
                    models.IntegerField(verbose_name="이중(부)전공이수필요학점"),
                ),
                ("required_gened_credit", models.IntegerField(verbose_name="교양이수필요학점")),
                (
                    "college",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.college",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ForeignTestRequired",
            fields=[
                (
                    "test_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="시험 아이디"
                    ),
                ),
                ("test_name", models.CharField(max_length=15, verbose_name="시험명")),
                (
                    "test_basic_score",
                    models.CharField(
                        max_length=20, null=True, verbose_name="요건 통과 기준 점수"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExtraForeignTest",
            fields=[
                (
                    "extra_test_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="기타시험 아이디"
                    ),
                ),
                (
                    "extra_test_name",
                    models.CharField(max_length=30, verbose_name="기타시험 이름"),
                ),
                (
                    "extra_test_basic_score",
                    models.CharField(max_length=20, null=True, verbose_name="기준"),
                ),
                (
                    "extra_test_gubun",
                    models.CharField(max_length=20, verbose_name="졸시/자격증"),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=200,
                        null=True,
                        verbose_name="추가정보/예를 들면 이중만 조건 다른 경우",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MajorSubjectCompleted",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("grade", models.CharField(max_length=5, verbose_name="성적")),
                ("retry_yn", models.BooleanField(default=False, verbose_name="재수강 여부")),
                ("school_year", models.IntegerField(verbose_name="학년/학기")),
                ("completed_year", models.CharField(max_length=5, verbose_name="수강년도")),
                (
                    "subject_department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.subjectdepartment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "subject_department")},
            },
        ),
        migrations.CreateModel(
            name="GeneralSubjectCompleted",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("grade", models.CharField(max_length=5, verbose_name="성적")),
                ("retry_yn", models.BooleanField(default=False, verbose_name="재수강 여부")),
                ("school_year", models.IntegerField(verbose_name="학년/학기")),
                ("completed_year", models.CharField(max_length=5, verbose_name="수강년도")),
                (
                    "subject_gened",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.subjectgened",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "subject_gened")},
            },
        ),
        migrations.CreateModel(
            name="ExceptionGenedSubject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comparison_code",
                    models.CharField(max_length=50, verbose_name="대체 과목코드"),
                ),
                (
                    "comparison_name",
                    models.CharField(max_length=20, verbose_name="대체 과목명"),
                ),
                (
                    "code_match",
                    models.BooleanField(default=False, verbose_name="코드값 일치"),
                ),
                (
                    "name_match",
                    models.BooleanField(default=False, verbose_name="과목명 일치"),
                ),
                (
                    "subject_gened_required",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.subjectgenedrequired",
                    ),
                ),
            ],
            options={
                "unique_together": {("subject_gened_required", "comparison_code")},
            },
        ),
        migrations.CreateModel(
            name="ExceptionDepartmentSubject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comparison_code",
                    models.CharField(max_length=50, verbose_name="대체 과목코드"),
                ),
                (
                    "comparison_name",
                    models.CharField(max_length=20, verbose_name="대체 과목명"),
                ),
                (
                    "code_match",
                    models.BooleanField(default=False, verbose_name="코드값 일치"),
                ),
                (
                    "name_match",
                    models.BooleanField(default=False, verbose_name="과목명 일치"),
                ),
                (
                    "subject_department_required",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.subjectdepartmentrequired",
                    ),
                ),
            ],
            options={
                "unique_together": {("subject_department_required", "comparison_code")},
            },
        ),
    ]
