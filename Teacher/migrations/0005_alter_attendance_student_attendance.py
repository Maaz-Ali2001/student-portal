# Generated by Django 4.2.4 on 2023-09-09 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0004_remove_attendance_attendance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_student',
            name='attendance',
            field=models.BooleanField(default=False),
        ),
    ]