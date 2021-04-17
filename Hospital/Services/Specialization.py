from Doctor.models.SpecializationData import SpecializationData
from HealthBackendProject.StatusCode import StatusCode
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, IntegrityError
from Hospital.models import HospitalSpecializationData
from Hospital.Services import logger

def addSpecialization(self, name) -> SpecializationData:
    try:
        data = SpecializationData(specialization=name)
        data.save()
        return data
    except:
        return None

def createSpecialization(self, name):
    json_data = {}
    try:
        data = SpecializationData.objects.get(specialization=name)
        json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'specialization already exists'}
    except ObjectDoesNotExist:
        if addSpecialization(name=name) is not None:
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'successfully added specialization'}
        else:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'somehting went wrong'}
    except IntegrityError as e:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
    except:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'somehting went wrong'}
    return json_data

def getSpecializationListBy(self, hospitalID):
    json_data = {}
    try:
        hospSpecialization = HospitalSpecializationData.objects.filter(hospital_id=hospitalID)
        data = []
        for item in hospSpecialization:
            specialization = SpecializationData.objects.get(id=item.specialization_id)
            data.append({'id': item.specialization_id, 'specialization': specialization.specialization})
        json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': data}
    except ObjectDoesNotExist:
        json_data = {'code': StatusCode.HTTP_403_FORBIDDEN.value, 'message': "no data found"}
    return json_data

def getSpecializationList():
    json_data = {}
    try:
        specializationData = SpecializationData.objects.all()
        data = []
        for result in specializationData:
            data.append({'id': result.id, 'name': result.specialization})
        json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': data}
    except ObjectDoesNotExist:
        json_data = {'code': StatusCode.HTTP_403_FORBIDDEN.value, 'message': "No data found"}
    return json_data
