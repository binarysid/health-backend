from django.db import models
from Doctor.models.SpecializationData import SpecializationData
from .HospitalData import HospitalData

class HospitalSpecializationData(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(HospitalData, on_delete=models.DO_NOTHING)
    specialization = models.ForeignKey(SpecializationData, on_delete=models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'hospital_specialization'
