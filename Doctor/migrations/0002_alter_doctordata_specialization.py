# Generated by Django 3.2 on 2021-04-16 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordata',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Doctor.specializationdata'),
        ),
    ]
