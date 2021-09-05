from django.db import models
from HealthBackendProject import MediaDirGen


class HospitalData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    license_no = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255,unique=True)
    lat = models.FloatField(max_length=255, blank=True, null=True)
    lng = models.FloatField(max_length=255, blank=True, null=True)
    logo = models.FileField(blank=True, null=True, upload_to=MediaDirGen.HOSPITAL_PROFILE_ROOT)
    class Meta:
        # managed = False
        db_table = 'hospital'

