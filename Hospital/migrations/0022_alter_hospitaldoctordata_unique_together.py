# Generated by Django 3.2 on 2021-08-26 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0008_auto_20210806_0847'),
        ('Hospital', '0021_hospitaldoctordata_time_spent_per_patient'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='hospitaldoctordata',
            unique_together={('doctor', 'hospital')},
        ),
    ]