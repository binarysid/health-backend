from django.db import models
from HealthBackendProject import MediaDirGen

class PatientData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(unique=True,max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    n_id = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    notification_reg_token = models.CharField(max_length=255, blank=True, null=True)
    photo = models.FileField(blank=True, null=True, upload_to=MediaDirGen.PATIENT_PROFILE_ROOT)

    class Meta:
        #managed = False
        db_table = 'patient'