# Generated by Django 3.2 on 2021-04-24 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0002_alter_doctordata_specialization'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctordata',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='doctor//profile//'),
        ),
    ]
