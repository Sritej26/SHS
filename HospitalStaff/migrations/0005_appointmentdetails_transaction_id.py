# Generated by Django 4.0.1 on 2022-04-04 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalStaff', '0004_delete_hospitalstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentdetails',
            name='transaction_id',
            field=models.CharField(default='#C', max_length=100),
        ),
    ]
