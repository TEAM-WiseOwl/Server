# Generated by Django 4.2 on 2024-11-20 02:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("requirements", "0002_alter_exceptiongenedsubject_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="openingsemester",
            name="subject_year",
        ),
        migrations.AlterField(
            model_name="openingsemester",
            name="subject_semester",
            field=models.CharField(max_length=10, verbose_name="개설학기"),
        ),
    ]