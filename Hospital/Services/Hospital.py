from Hospital.models.HospitalData import HospitalData,HospitalSerializer
from rest_framework.views import APIView
from HealthBackendProject.Response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from HealthBackendProject.Service import ExceptionLogger

class HospitalList(APIView):
    def post(self, request, format=None):
        try:
            data = HospitalData.objects.all()
            serializer = HospitalSerializer(data, many=True, context={"request": request})
            return Response(code=status.HTTP_200_OK,message='success',data=serializer.data)
        except ObjectDoesNotExist:
            return Response(code=status.HTTP_400_BAD_REQUEST, message='no hospital found')
        except Exception as e:
            ExceptionLogger.track(e=e)
            return Response(code=status.HTTP_400_BAD_REQUEST, message='something went wrong')
