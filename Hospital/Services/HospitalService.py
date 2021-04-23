from Hospital.Services import logger
from Hospital.models.HospitalData import HospitalData
from HealthBackendProject.StatusCode import StatusCode
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, IntegrityError
from HealthBackendProject import Utility
from HealthBackendProject import LogHandler
logger = LogHandler.getLogHandler(filename='hospital.log')

def editHospitalInfo(id,logo):
    json_data = {}
    try:
        data = HospitalData.objects.get(id=id)
        if logo is not None:
            if data.logo:
                Utility.removeFile(data.logo.path)
            data.logo = Utility.convertBase64ToImageFile(logo, id=id)
        data.save()
        json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'info updated'}
    except IntegrityError as e:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
    except:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'no account found'}
    return json_data

