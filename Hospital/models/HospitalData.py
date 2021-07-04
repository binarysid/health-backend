from django.db import models
from HealthBackendProject import MediaDirGen
from rest_framework import serializers

class HospitalData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    license_no = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255)
    lat = models.FloatField(max_length=255, blank=True, null=True)
    lng = models.FloatField(max_length=255, blank=True, null=True)
    logo = models.FileField(blank=True, null=True, upload_to=MediaDirGen.HOSPITAL_PROFILE_ROOT)
    class Meta:
        # managed = False
        db_table = 'hospital'

class HospitalSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField('get_logo_url')

    class Meta:
        model = HospitalData
        exclude = ('password','license_no','logo')

    def get_logo_url(self, hospital):
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(hospital.logo.url)
        except:
            return ''
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return HospitalData.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance