# Generated by Django 3.2 on 2021-08-26 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0022_alter_hospitaldoctordata_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitaldoctordata',
            name='max_patient_per_day',
        ),
    ]