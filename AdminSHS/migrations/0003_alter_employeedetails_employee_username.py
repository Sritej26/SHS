# Generated by Django 4.0.1 on 2022-04-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminSHS', '0002_employeedetails_employee_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedetails',
            name='employee_username',
            field=models.CharField(max_length=255),
        ),
    ]
