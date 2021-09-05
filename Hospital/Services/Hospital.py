from Hospital.models.HospitalData import HospitalData
from Hospital.serializers.HospitalSerializer import HospitalSerializer
#from rest_framework.views import APIView
from HealthBackendProject.Response import Response
from rest_framework import status, mixins, generics
from HealthBackendProject.Service import ExceptionLogger
from HealthBackendProject.HashPassword import HashPassword
from django.core.exceptions import ObjectDoesNotExist
from HealthBackendProject import Utility
from django.core.exceptions import ObjectDoesNotExist

class HospitalList(generics.GenericAPIView,mixins.ListModelMixin):
    # queryset = HospitalData.objects.all()
    # serializer_class = HospitalSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get(self, request):
        try:
            hospital = HospitalData.objects.all()
            serializer = HospitalSerializer(hospital,many=True)
            if hospital:
                return Response(code=status.HTTP_200_OK,message='success',data=serializer.data)
            else:
                return Response(code=status.HTTP_400_BAD_REQUEST, message='no hospital found')
        except Exception as e:
            ExceptionLogger.track(e=e)
            return Response(code=status.HTTP_400_BAD_REQUEST, message='something went wrong')

    def post(self,request):
        try:
            licenseNo = request.data['license_no']
            phone = request.data['phone']
            data = HospitalData.objects.get(license_no=licenseNo, phone=phone)
            return Response(code=status.HTTP_409_CONFLICT, message='account with this license_no or phone already exists')
        except ObjectDoesNotExist:
            if not request.POST._mutable:
                request.POST._mutable = True
            passwd = request.data['password']
            request.data['password'] = HashPassword.createPassword(passwd)
            serializer = HospitalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(code=status.HTTP_201_CREATED,message='success', data=serializer.data)
            return Response(code=status.HTTP_404_NOT_FOUND, message='Something went wrong')
        except Exception as e:
            ExceptionLogger.track(e=e)
            return Response(code=status.HTTP_404_NOT_FOUND, message='Something went wrong')

    def put(self,request):
        try:
            phone = request.data['phone']
            hospital = HospitalData.objects.get(phone=phone)
            if 'logo' in request.data:
                if hospital.logo:
                    Utility.removeFile(hospital.logo.path)
                hospital.logo = Utility.convertBase64ToImageFile(request.data['logo'], id=hospital.id)
            if 'password' in request.data:
                if not request.POST._mutable:
                    request.POST._mutable = True
                request.data['password'] = HashPassword.createPassword(request.data['password'])
            if 'lat' in request.data:
                lat = float(request.data['lat'])
                hospital.lat = lat
            if 'lng' in request.data:
                lng = float(request.data['lng'])
                hospital.lng = lng
            serializer = HospitalSerializer(hospital, data=request.data,
                                          partial=True)  # By default, serializers must be passed values for all required fields or they will raise validation errors. So we must use the partial argument in order to allow partial updates.
            if serializer.is_valid():
                serializer.save()
                return Response(code=status.HTTP_200_OK, message='successfully updated info')
            else:
                print(serializer.errors)
            return Response(code=status.HTTP_400_BAD_REQUEST, message='something went wrong')
        except ObjectDoesNotExist:
            return Response(code=status.HTTP_404_NOT_FOUND, message='user not found')
        except Exception as e:
            ExceptionLogger.track(e=e)
            return Response(code=status.HTTP_400_BAD_REQUEST, message='something went wrong')
