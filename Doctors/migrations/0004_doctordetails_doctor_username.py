# Generated by Django 4.0.1 on 2022-04-06 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0003_labtests_lab_report_labtests_lab_report_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctordetails',
            name='doctor_username',
            field=models.CharField(default='ds', max_length=100),
        ),
    ]
