from Doctor.models.DoctorData import DoctorData
from Hospital.models.HospitalDoctorData import HospitalDoctorData
from Doctor.serializers.DoctorSerializer import DoctorSerializer
from HealthBackendProject.Response import Response
from rest_framework import status,viewsets
from django.core.exceptions import ObjectDoesNotExist
from HealthBackendProject.Service import ExceptionLogger
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from HealthBackendProject import Utility
from Doctor.models.SpecializationData import SpecializationData
from Hospital.Services import HospitalService
from HealthBackendProject.HashPassword import HashPassword

class Doctor(viewsets.ViewSet):
    # parser_classes = [MultiPartParser,] # define media type here. global media type has been defined in settings.py as rest_framework.parsers.FormParser
    def destroy(self, request):
        try:
            data = DoctorData.objects.get(phone=request.data['phone'])
            if HashPassword.isValidPassword(request.data['password'], data.password):
                data.delete()
                return Response(code=status.HTTP_200_OK,
                                message='user removed successfully')

            else:
                return Response(code=status.HTTP_404_NOT_FOUND,
                                message='password doesnot match')
        except ObjectDoesNotExist:
            return Response(code=status.HTTP_404_NOT_FOUND,
                            message='user not found')
        except Exception as e:
            ExceptionLogger.track(e=e)
            return Response(code=status.HTTP_400_BAD_REQUEST,
                            message='something went wrong')

    def update(self,request):
        try:
            doctor = DoctorData.objects.get(phone=request.data['phone'])
            if 'password' in request.data and doctor.password is None:
                if not request.POST._mutable:
                    request.POST._mutable = True
                request.data['password'] = HashPassword.createPassword(request.data['password'])
            if 'photo' in request.data:
                if doctor.photo:
                    Utility.removeFile(doctor.photo.path)
                doctor.photo = Utility.convertBase64ToImageFile(request.data['photo'], id=doctor.id)
            if 'specialization_id' in request.data:
                doctor.specialization = SpecializationData.objects.get(id=request.data['specialization_id'])
            serializer = DoctorSerializer(doctor, data=request.data, partial=True) #By default, serializers must be passed values for all required fields or they will raise validation errors. So we must use the partial argument in order to allow partial updates.
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

    def list(self,request):
        try:
            doctors = []
            hospital_id = None
            if 'hospital_id' in request.data:
                hospital_id = request.data['hospital_id']
                filteredDoctor = HospitalDoctorData.objects.filter(hospital_id=hospital_id)
                if filteredDoctor:
                    for doctor in filteredDoctor:
                        if 'specialization_id' in request.data:
                            doctor_data = self.getDoctorBySpecialization(doctorID=doctor.doctor_id,specializationID=request.data['specialization_id'])
                            if doctor_data is None:
                                continue
                        else:
                            doctor_data = DoctorData.objects.get(id=doctor.doctor_id)
                        doctors.append(doctor_data)
            elif 'specialization_id' in request.data:
                doctors = DoctorData.objects.filter(specialization_id=request.data['specialization_id'])
            else:
                doctors = DoctorData.objects.all()
            if doctors:
                serializer = DoctorSerializer(doctors,many=True, context={"hospital_id": hospital_id,"request": request})
                return Response(code=status.HTTP_200_OK, message='success',data=serializer.data)
            return Response(code=status.HTTP_404_NOT_FOUND, message='no doctor found')

        except ObjectDoesNotExist:
            return Response(code=status.HTTP_400_BAD_REQUEST, message='no doctor found')
        except Exception as e:
            ExceptionLogger.track(e=e)
            return Response(code=status.HTTP_400_BAD_REQUEST, message='something went wrong')

    def create(self,request):
        try:
            doctor = DoctorData.objects.get(reg_no=request.data['reg_no'],phone=request.data['phone'])
            return Response(code=status.HTTP_409_CONFLICT, message='account with this reg_no or phone already exists')
        except ObjectDoesNotExist:
            if 'password' in request.data:
                if not request.POST._mutable:
                    request.POST._mutable = True
                request.data['password'] = HashPassword.createPassword(request.data['password'])
            serializer = DoctorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(specialization_id=request.data['specialization_id'])
                if 'hospital_id' in request.data:
                    doctorId = DoctorData.objects.get(phone=request.data['phone']).id
                    response = HospitalService.doctorEntryOnHospitalList(hospitalID=request.data['hospital_id'],
                                                                         doctorID=doctorId)
                return Response(code=status.HTTP_201_CREATED, message='successfully registered', data=serializer.data)
            return Response(code=status.HTTP_400_BAD_REQUEST, message=serializer.errors)
        except Exception as e:
            ExceptionLogger.track(e=e)
            return Response(code=status.HTTP_400_BAD_REQUEST, message='something went wrong')

    def getDoctorBySpecialization(self,doctorID,specializationID):
        try:
            return DoctorData.objects.get(id=doctorID,specialization_id=specializationID)
        except:
            return None