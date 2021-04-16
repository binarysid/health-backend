from django.db import models
from Doctor.models.DoctorData import DoctorData
from .HospitalData import HospitalData
from .WeekData import WeekData

class HospitalDoctorScheduleData(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    is_available = models.IntegerField()
    week = models.ForeignKey(WeekData, on_delete=models.DO_NOTHING)
    hospital = models.ForeignKey(HospitalData, on_delete=models.DO_NOTHING, blank=True, null=True)
    doctor = models.ForeignKey(DoctorData, on_delete=models.DO_NOTHING)
    visit_start_time = models.CharField(max_length=255, blank=True, null=True)
    visit_end_time = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'hospital_doctor_schedule'
