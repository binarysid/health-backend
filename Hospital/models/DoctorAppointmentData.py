from django.db import models
from Doctor.models.DoctorData import DoctorData
from .HospitalData import HospitalData

class DoctorAppointmentData(models.Model):
    id = models.AutoField(primary_key=True)
    serial_no = models.IntegerField()
    doctor = models.ForeignKey(DoctorData, models.DO_NOTHING)
    hospital = models.ForeignKey(HospitalData, models.DO_NOTHING)
    visit_time = models.CharField(max_length=255, blank=True, null=True)
    visit_date = models.DateField()
    patient_name = models.CharField(max_length=255)
    patient_phone = models.CharField(max_length=255)
    patient_id = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'doctor_appointment'
        unique_together = (('doctor', 'hospital', 'visit_date', 'patient_phone'),)
