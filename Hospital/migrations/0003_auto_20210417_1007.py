# Generated by Django 3.2 on 2021-04-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0002_auto_20210416_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaldata',
            name='lat',
            field=models.FloatField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='hospitaldata',
            name='lng',
            field=models.FloatField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
