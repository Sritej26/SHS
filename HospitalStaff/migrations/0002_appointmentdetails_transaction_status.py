# Generated by Django 4.0.1 on 2022-04-02 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalStaff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentdetails',
            name='transaction_status',
            field=models.CharField(default='Pending', max_length=255),
        ),
    ]
