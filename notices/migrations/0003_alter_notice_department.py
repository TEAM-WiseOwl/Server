# Generated by Django 4.2 on 2024-11-17 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("requirements", "0002_alter_exceptiongenedsubject_unique_together"),
        ("notices", "0002_subscribe_subscribe_cfl_subscribe_subscribe_flex_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notice",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="requirements.department",
            ),
        ),
    ]
