from rest_framework import serializers
from Doctor.models.DoctorData import DoctorData
from Doctor.models.SpecializationData import SpecializationData
from Hospital.Services import HospitalService

class DoctorSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('get_logo_url')
    specialization = serializers.SerializerMethodField('get_specialization')
    profile_completion_ratio = serializers.SerializerMethodField('get_profile_completion_ratio')

    class Meta:
        model = DoctorData
        exclude = ('created_on','updated_on')
        extra_kwargs = {
            'reg_no': {'write_only': True},
            'password': {'write_only': True},
            'nid': {'write_only': True}
        }

    def get_logo_url(self, data):
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(data.photo.url)
        except:
            return ''

    def get_specialization(self, data):
        try:
            specData = SpecializationData.objects.get(id=data.specialization.id)
            return specData.specialization
        except:
            return ""

    def get_profile_completion_ratio(self,data):
        hospital_id = self.context.get('hospital_id')
        if hospital_id is None:
            return 100;
        return HospitalService.doctor_profile_completion_ratio(hospital_id=hospital_id, doctor_id=data.id)