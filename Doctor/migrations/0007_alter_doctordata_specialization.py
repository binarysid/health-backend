# Generated by Django 3.2 on 2021-08-04 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0006_alter_doctordata_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordata',
            name='specialization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Doctor.specializationdata'),
        ),
    ]