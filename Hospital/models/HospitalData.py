from django.db import models

class HospitalData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    license_no = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=255)
    lat = models.FloatField(unique=True, max_length=255, blank=True, null=True)
    lng = models.FloatField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'hospital'

