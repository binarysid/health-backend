# Generated by Django 3.2 on 2021-04-21 14:59

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0006_alter_hospitaldata_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitaldata',
            name='logo',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to='hospital'),
        ),
    ]
