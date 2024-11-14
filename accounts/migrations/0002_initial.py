<<<<<<< HEAD
# Generated by Django 4.2 on 2024-11-13 06:54
=======
# Generated by Django 4.2 on 2024-11-14 06:29
>>>>>>> cc604fefa7670a6ce8eda3e9aec04ca90ecf2cf0

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("requirements", "0001_initial"),
        ("accounts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="requeststunumber",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="request_department_id",
                to="requirements.department",
                verbose_name="학과 아이디",
            ),
        ),
        migrations.AddField(
            model_name="requeststunumber",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="request_user_id",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="double_or_minor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="double_minor",
                to="requirements.department",
                verbose_name="이중/부전공 학과",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="double_or_minor_college",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="double_minor_college",
                to="requirements.college",
                verbose_name="이중/부전공 대학",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="major",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="major",
                to="requirements.department",
                verbose_name="학과",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="major_college",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="major_college",
                to="requirements.college",
                verbose_name="대학",
            ),
        ),
    ]
