from Doctor.Service import logger
from django.core.exceptions import ObjectDoesNotExist
from HealthBackendProject.Service import ExceptionLogger
from HealthBackendProject.Response import Response
from rest_framework import status
from ..models.DoctorData import DoctorData
from HealthBackendProject.HashPassword import HashPassword
from ..models.SpecializationData import SpecializationData

def login(phone, password, request):
    try:
        data = DoctorData.objects.get(phone=phone)
        if HashPassword.isValidPassword(password, data.password):
            return Response(code=status.HTTP_200_OK, message='success',data={"id": data.id,'name': data.name,'photo': request.build_absolute_uri(data.photo.url) if data.photo else ''})
        else:
            return Response(code=status.HTTP_404_NOT_FOUND, message='password doesnt match')
    except ObjectDoesNotExist:
        return Response(code=status.HTTP_404_NOT_FOUND, message='user not found')
    except Exception as e:
        ExceptionLogger.track(e=e)
        return Response(code=status.HTTP_400_BAD_REQUEST, message='something went wrong')

    def getSpecializationObj(self,id):
        try:
            return SpecializationData.objects.get(id=id)
        except:
            return None