from django.db import models
from Doctor.models.DoctorData import DoctorData
from .HospitalData import HospitalData

class HospitalDoctorData(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(HospitalData,  on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(DoctorData, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=255, blank=True, null=True)
    visit_fee = models.CharField(max_length=255, blank=True, null=True)
    visit_start_time = models.CharField(max_length=255, blank=True, null=True)
    visit_end_time = models.CharField(max_length=255, blank=True, null=True)
    visit_start_day = models.CharField(max_length=255, blank=True, null=True)
    visit_end_day = models.CharField(max_length=255, blank=True, null=True)
    room_no = models.CharField(max_length=255, blank=True, null=True)
    max_patient_per_day = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'hospital_doctor'
