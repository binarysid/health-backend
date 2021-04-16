from django.db import models

class SpecializationData(models.Model):
    specialization = models.CharField(unique=True, max_length=255)
    id = models.AutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'specialization'

