from django.db import models
from .SpecializationData import SpecializationData
from HealthBackendProject import MediaDirGen

class DoctorData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    reg_no = models.CharField(unique=True,max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    degrees = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=255)
    nid = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.ForeignKey(SpecializationData, on_delete=models.DO_NOTHING, null=True)
    photo = models.FileField(blank=True, null=True, upload_to=MediaDirGen.DOCTOR_PROFILE_ROOT)

    class Meta:
        # managed = False
        db_table = 'doctor'
