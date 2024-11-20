# Generated by Django 4.2 on 2024-11-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("requirements", "0003_remove_openingsemester_subject_year_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="majorsubjectcompleted",
            name="completed_year",
            field=models.CharField(max_length=10, verbose_name="수강년도"),
        ),
        migrations.AlterField(
            model_name="majorsubjectcompleted",
            name="grade",
            field=models.CharField(default="A+", max_length=5, verbose_name="성적"),
        ),
    ]
