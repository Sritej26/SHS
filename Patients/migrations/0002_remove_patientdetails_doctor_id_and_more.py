# Generated by Django 4.0.1 on 2022-02-13 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientdetails',
            name='doctor_id',
        ),
        migrations.AddField(
            model_name='patientdetails',
            name='patient_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
