# Generated by Django 3.2 on 2021-05-10 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0017_auto_20210505_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaldata',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
