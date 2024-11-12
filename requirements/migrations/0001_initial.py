# Generated by Django 4.2 on 2024-11-09 13:44

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
                ("college_required_credit", models.IntegerField(verbose_name="졸업이수학점")),
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
                    "subject_department_room",
                    models.CharField(max_length=10, verbose_name="강의실"),
                ),
                (
                    "subject_department_date",
                    models.CharField(max_length=14, verbose_name="강의시간"),
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
                    "subject_gened_room",
                    models.CharField(max_length=10, verbose_name="강의실"),
                ),
                (
                    "subject_gened_date",
                    models.CharField(max_length=14, verbose_name="강의시간"),
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
                ("required_credit_sn", models.IntegerField(verbose_name="학번(이상)")),
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
                ("test_basic_score", models.IntegerField(verbose_name="요건 통과 기준 점수")),
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
                    "subject_gened_required_db",
                    models.BooleanField(default=False, verbose_name="이중전공 여부"),
                ),
                (
                    "subject_gened_required_sn",
                    models.IntegerField(verbose_name="학번(이상)"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
                (
                    "subject_gened",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.subjectgened",
                    ),
                ),
            ],
            options={
                "unique_together": {("subject_gened", "department")},
            },
        ),
        migrations.CreateModel(
            name="SubjectDepartmentRequired",
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
                    "subject_gened_required_db",
                    models.BooleanField(default=False, verbose_name="이중전공 여부"),
                ),
                (
                    "subject_gened_required_sn",
                    models.IntegerField(verbose_name="학번(이상)"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.department",
                    ),
                ),
                (
                    "subject_requirement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="requirements.subjectdepartment",
                    ),
                ),
            ],
            options={
                "unique_together": {("subject_requirement", "department")},
            },
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
    ]