# Generated by Django 4.2 on 2024-11-17 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notices", "0003_alter_notice_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notice",
            name="notice_link",
            field=models.URLField(max_length=700, verbose_name="알림 url"),
        ),
    ]
