# Generated by Django 5.0.7 on 2024-12-04 01:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0008_alter_profile_major_alter_profile_major_college_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_agreement",
            field=models.BooleanField(default=None, null=True),
        ),
    ]
