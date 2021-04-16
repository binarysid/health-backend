from django.db import models

class WeekData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        # managed = False
        db_table = 'week'