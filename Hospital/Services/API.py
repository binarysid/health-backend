from django.db import connection,IntegrityError
from django.http import HttpResponse,JsonResponse
from Hospital.HospitalQuery import HospitalQuery
import json
from rest_framework.decorators import api_view
from HealthBackendProject.StatusCode import StatusCode
from Hospital.APIKey import ApiKey
from Hospital.Services import logger
from Hospital.Services import Specialization
from HealthBackendProject import LogHandler
from Hospital.Services import HospitalService
from HealthBackendProject.Service import ExceptionLogger
from Hospital.serializers.HospitalDoctorSerializer import HospitalDoctorSerializer
from HealthBackendProject.Response import Response
from rest_framework import status
from Doctor.models.DoctorData import DoctorData
from Hospital.models.HospitalData import HospitalData
from Hospital.models.HospitalDoctorData import HospitalDoctorData

@api_view(['POST'])
def GetDoctorProfileCompletionRatio(request):
    # version = request.headers['version']
    doctorID = int(request.POST['doctor_id'])
    hospitalID = int(request.POST['hospital_id'])
    json_data = HospitalService.get_doctor_profile_completion(hospital_id=hospitalID,doctor_id=doctorID)
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def CancelAppointment(request):
    # version = request.headers['version']
    doctorID = int(request.POST['doctor_id'])
    hospitalID = int(request.POST['hospital_id'])
    date = request.POST.get('date', None)
    json_data = HospitalService.cancelDoctorAppointment(hospitalID=hospitalID,doctorID=doctorID,date=date)
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def Login(request):
    # version = request.headers['version']
    phone = request.POST.get('phone', None)
    password = request.POST.get('password', None)
    json_data = HospitalService.login(request=request,phone=phone, password=password)
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def createWeekList(request):
    HospitalService.createWeekList()

@api_view(['POST'])
def UpdateWeek(request):
    try:
        id = int(request.POST['id'])
        name = request.POST['name']
        json_data = HospitalService.updateWeekBy(id, name)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def AddDoctor(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        json_data = HospitalService.doctorEntryOnHospitalList(doctorID, hospitalID)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def removeDoctor(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        json_data = HospitalService.removeDoctorFromHospital(doctorID, hospitalID)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def SpecializationList(request):
    hospitalID = request.POST.get('hospital_id',None)
    if hospitalID is not None:
        hospitalID = int(hospitalID)
        json_data = Specialization.getSpecializationListBy(hospitalID)
    else:
        json_data = Specialization.getSpecializationList()
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def HospitalRegistration(request):
    try:
        name = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']
        licenseNo = request.POST['license_no']
        logo = request.POST.get('logo',None)
        json_data = HospitalService.executeRegister(request,name, phone, password, licenseNo,logo=logo)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def UpdateInfo(request):
    try:
        id = int(request.POST['id'])
        name = request.POST.get('name',None)
        phone = request.POST.get('phone',None)
        password = request.POST.get('password',None)
        lat = request.POST.get('lat',None)
        lng = request.POST.get('lng',None)
        logo = request.POST.get('logo',None)
        email = request.POST.get('email', None)
        address = request.POST.get('address', None)
        json_data = HospitalService.infoUpdate(request=request,name=name,id=id,
                                               phone=phone,password=password,
                                               lat=lat,lng=lng,
                                               logo=logo,email=email,
                                               address=address)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")


@api_view(['POST'])
def CreateSpecialization(request):
    name = request.POST['name']
    json_data = Specialization.createSpecialization(name=name)
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def ConvertExistingNonHashedPasswordToHash(request):
    try:
        password = request.POST.get('password',None)
        phone = request.POST.get('phone', None)
        json_data = HospitalService.updateExistingNonHashedPasswordToHash(password=password,phone=phone)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def GetDoctorAppointment(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        date = request.POST.get('date',None)
        json_data = HospitalService.getAppointments(doctorID=doctorID,hospitalID=hospitalID,date=date)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def AddSpecializationToHospital(request):
    specializationID = request.POST.get('specialization_id',None)
    specialization = request.POST.get('specialization',None)
    hospitalID = int(request.POST['hospital_id'])
    json_data = Specialization.attachSpecializationToHospital(specializationID=specializationID,specializationName=specialization,hospitalID=hospitalID)
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def RemoveSpecializationFromHospital(request):
    try:
        specializationID = int(request.POST['specialization_id'])
        hospitalID = int(request.POST['hospital_id'])
        json_data = HospitalService.detachSpecializationFromHospital(specializationID=specializationID,hospitalID=hospitalID)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def UpdateDoctorInfoInHospital(request):
    try:
        data = HospitalDoctorData.objects.get(
            doctor_id = request.data['doctor_id'],
            hospital_id= request.data['hospital_id']
        )
        serializer = HospitalDoctorSerializer(data,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(
                doctor=DoctorData.objects.get(id=request.data['doctor_id']),
                hospital=HospitalData.objects.get(id=request.data['hospital_id'])
            )
            return Response(code=status.HTTP_200_OK, message='successfully updated info')
        return Response(code=status.HTTP_404_NOT_FOUND, message=serializer.error)
    except Exception as e:
        ExceptionLogger.track(e=e)
        return Response(code=status.HTTP_404_NOT_FOUND, message='Something went wrong')

@api_view(['POST'])
def RemoveDoctorScheduleFromHospital(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        weekID = int(request.POST['week_id'])
        json_data = HospitalService.removeDoctorScheduleFromHospital(doctorID, hospitalID, weekID)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def UpdateDoctorScheduleForHospital(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        isAvailable = request.POST.get('is_available',None)
        if isAvailable is not None:
            isAvailable = int(isAvailable)
        weekID = int(request.POST['week_id'])
        startTime = request.POST.get('start_time',None)
        endTime = request.POST.get('end_time',None)
        json_data = HospitalService.updateDoctorScheduleForHospital(isAvailable=isAvailable, hospitalID=hospitalID,doctorID=doctorID,weekID=weekID,startTime=startTime,endTime=endTime)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def AddDoctorScheduleDateToHospital(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        weekID = int(request.POST['week_id'])
        date = request.POST.get('date',None)
        startTime = request.POST.get('start_time',None)
        endTime = request.POST.get('end_time',None)
        json_data = HospitalService.executeAddDoctorScheduleDateToHospital(doctorID, hospitalID, weekID,
                                                                                    startTime,endTime)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def DoctorSchedules(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        json_data = HospitalService.getDoctorsScheduleFromHospital(doctorID, hospitalID)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def CreateDoctorAppointment(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        visitDate = request.POST['visit_date']
        patientName = request.POST['patient_name']
        patientPhone = request.POST['patient_phone']
        patientID = request.POST.get('patient_id',None)
        if patientID !=None:
            patientID = int(patientID)
        json_data = HospitalService.executeDoctorAppointment(doctorID, hospitalID, visitDate, patientName,
                                                                      patientPhone, patientID)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def DoctorProfile(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        json_data = HospitalService.getDoctorProfileBy(hospitalID, doctorID,request)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def UpdateDoctorProfile(request):
    try:
        doctorID = int(request.POST['doctor_id'])
        hospitalID = int(request.POST['hospital_id'])
        name = request.POST.get('name')
        degrees = request.POST.get('degrees')
        visitFee = request.POST.get('visit_fee')
        roomNo = request.POST.get('room_no')
        maxPatientPerDay = request.POST.get('max_patient_per_day')
        if maxPatientPerDay is not None and maxPatientPerDay != '':
            maxPatientPerDay = int(maxPatientPerDay)
        specializationID = request.POST.get('specialization_id')
        if specializationID is not None and specializationID != '':
            specializationID = int(specializationID)
        specialization = request.POST.get('specialization')
        photo = request.POST.get('photo',None)
        json_data = HospitalService.updateDoctorProfileBy(hospitalID, doctorID,
                                                                   name,degrees,visitFee,
                                                                   roomNo,maxPatientPerDay,
                                                                   specializationID,specialization,photo)
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return HttpResponse(json.dumps(json_data), content_type="application/json")

@api_view(['POST'])
def GetWeekLists(request):
    try:
        doctorID = request.POST.get('doctor_id',None)
        hospitalID = request.POST.get('hospital_id',None)
        if hospitalID !=None and doctorID !=None:
            json_data = HospitalService.getAllWeeksBy(hospitalID=hospitalID,doctorID=doctorID)
        else:
            json_data = HospitalService.getAllWeeks()
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

    return HttpResponse(json.dumps(json_data), content_type="application/json")

