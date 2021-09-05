from rest_framework import serializers
from Hospital.models.HospitalData import HospitalData

class HospitalSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField('get_logo_url')

    class Meta:
        model = HospitalData
        exclude = ('logo',)
        extra_kwargs = {
            'license_no': {'write_only': True},
            'password': {'write_only': True}
        }

    def get_logo_url(self, hospital):
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(hospital.logo.url)
        except:
            return ''