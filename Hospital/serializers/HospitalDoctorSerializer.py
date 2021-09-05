from rest_framework import serializers
from Hospital.models.HospitalDoctorData import HospitalDoctorData

class HospitalDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDoctorData
        exclude = ('hospital','doctor',)