from django.db import connection,IntegrityError
from django.http import HttpResponse
from .HospitalQuery import HospitalQuery
import json
from django.views.decorators.csrf import csrf_exempt
from HealthBackendProject.StatusCode import StatusCode
from .APIKey import ApiKey
import logging

class API:
    def __init__(self):
        self.logger = self.getLogHandler()
        self.queryConnectionPool = HospitalQuery(logger=self.logger)

    def getLogHandler(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s]: %(levelname)s: %(name)s: %(funcName)s: %(filename)s: line no- %(lineno)s : %(message)s')
        fileHandler = logging.FileHandler('hospital.log')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        return logger

    @csrf_exempt
    def Login(self,request):
        # version = request.headers['version']
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        jsonData = self.queryConnectionPool.login(phone, password)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def HospitalList(self,request):
        try:
            jsonData = self.queryConnectionPool.getHospitalList()
        except IntegrityError as e:
            jsonData = {'code':StatusCode.HTTP_400_BAD_REQUEST.value, 'message':e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def createWeekList(self,request):
        self.queryConnectionPool.createWeekList()

    @csrf_exempt
    def UpdateWeek(self,request):
        try:
            id = int(request.POST['id'])
            name = request.POST['name']
            jsonData = self.queryConnectionPool.updateWeekBy(id, name)
        except IntegrityError as e:
            jsonData = {'code':StatusCode.HTTP_400_BAD_REQUEST.value, 'message':e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def AddDoctor(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            jsonData = self.queryConnectionPool.doctorEntryOnHospitalList(doctorID, hospitalID)
        except IntegrityError as e:
            jsonData = {'code':StatusCode.HTTP_400_BAD_REQUEST.value, 'message':e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def removeDoctor(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            jsonData = self.queryConnectionPool.removeDoctorFromHospital(doctorID, hospitalID)
        except IntegrityError as e:
            jsonData = {'code':StatusCode.HTTP_400_BAD_REQUEST.value, 'message':e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def SpecializationList(self,request):
        try:
            hospitalID = int(request.POST['hospital_id'])
            jsonData = self.queryConnectionPool.getSpecializationListBy(hospitalID)
        except IntegrityError as e:
            jsonData = {'code':StatusCode.HTTP_400_BAD_REQUEST.value, 'message':e.args[1]}
        except:
            jsonData = self.queryConnectionPool.getSpecializationList()
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def HospitalRegistration(self,request):
        try:
            name = request.POST['name']
            phone = request.POST['phone']
            password = request.POST['password']
            licenseNo = request.POST['license_no']
            jsonData = self.queryConnectionPool.executeRegister(name, phone, password, licenseNo)
        except IntegrityError as e:
            self.logger.debug(e.args[1])
            jsonData = {'code':StatusCode.HTTP_400_BAD_REQUEST.value, 'message':e.args[1]}
        except:
            self.logger.debug('post request field parse error')
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def CreateSpecialization(self,request):
        try:
            name = request.POST['name']
            jsonData = self.queryConnectionPool.createSpecialization(name)
        except IntegrityError as e:
            jsonData = {'code':StatusCode.HTTP_400_BAD_REQUEST.value, 'message':e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def ConvertExistingNonHashedPasswordToHash(self,request):
        try:
            password = request.POST.get('password',None)
            phone = request.POST.get('phone', None)
            jsonData = self.queryConnectionPool.updateExistingNonHashedPasswordToHash(password=password,phone=phone)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "missing required param"}

        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def GetDoctorAppointment(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            date = request.POST.get('date',None)
            jsonData = self.queryConnectionPool.getAppointmentsby(doctorID=doctorID,hospitalID=hospitalID,date=date)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "missing required param"}

        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def AddSpecializationToHospital(self,request):
        try:
            specializationID = int(request.POST['specialization_id'])
            hospitalID = int(request.POST['hospital_id'])
            jsonData = self.queryConnectionPool.attachSpecializationToHospital(specializationID=specializationID,hospitalID=hospitalID)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def RemoveSpecializationFromHospital(self,request):
        try:
            specializationID = int(request.POST['specialization_id'])
            hospitalID = int(request.POST['hospital_id'])
            jsonData = self.queryConnectionPool.detachSpecializationFromHospital(specializationID=specializationID,hospitalID=hospitalID)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def UpdateDoctorInfoInHospital(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            visitFee = request.POST.get(ApiKey.visitFee,None)
            startTime = request.POST.get('start_time',None)
            endTime = request.POST.get('end_time',None)
            startDay = request.POST.get('start_day',None)
            endDay = request.POST.get('end_day',None)
            roomNo = request.POST.get(ApiKey.roomNo,None)
            phone = request.POST.get('phone',None)
            maxPat = request.POST.get('max_patient_per_day',None)
            maxPatientPerDay = maxPat if maxPat == None else int(maxPat)
            jsonData = self.queryConnectionPool.updateDoctorInfoForHospital(doctorID, hospitalID, phone, visitFee,
                                                                            startTime, endTime, startDay, endDay,
                                                                          roomNo, maxPatientPerDay)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "something went wrong"}

        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def RemoveDoctorScheduleFromHospital(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            weekID = int(request.POST['week_id'])
            jsonData = self.queryConnectionPool.removeDoctorScheduleFromHospital(doctorID, hospitalID, weekID)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "missing required param"}

        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def UpdateDoctorScheduleForHospital(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            isAvailable = request.POST.get('is_available',None)
            if isAvailable is not None:
                isAvailable = int(isAvailable)
            weekID = int(request.POST['week_id'])
            startTime = request.POST.get('start_time',None)
            endTime = request.POST.get('end_time',None)
            jsonData = self.queryConnectionPool.updateDoctorScheduleForHospital(isAvailable=isAvailable, hospitalID=hospitalID,doctorID=doctorID,weekID=weekID,startTime=startTime,endTime=endTime)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "missing required param"}

        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def AddDoctorScheduleDateToHospital(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            weekID = int(request.POST['week_id'])
            date = request.POST.get('date',None)
            startTime = request.POST.get('start_time',None)
            endTime = request.POST.get('end_time',None)
            jsonData = self.queryConnectionPool.executeAddDoctorScheduleDateToHospital(doctorID, hospitalID, weekID,
                                                                                   startTime,endTime)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "missing required param"}

        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def DoctorSchedules(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            jsonData = self.queryConnectionPool.getDoctorsScheduleFromHospital(doctorID, hospitalID)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def CreateDoctorAppointment(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            visitTime = request.POST.get('visit_time',None)
            visitDate = request.POST['visit_date']
            patientName = request.POST['patient_name']
            patientPhone = request.POST['patient_phone']
            patientID = request.POST.get('patient_id',None)
            if patientID !=None:
                patientID = int(patientID)
            jsonData = self.queryConnectionPool.executeDoctorAppointment(doctorID, hospitalID, visitTime, visitDate, patientName,
                                                                    patientPhone, patientID)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def DoctorProfile(self,request):
        try:
            doctorID = int(request.POST['doctor_id'])
            hospitalID = int(request.POST['hospital_id'])
            jsonData = self.queryConnectionPool.getDoctorProfileBy(hospitalID, doctorID)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "missing required param"}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def UpdateDoctorProfile(self,request):
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
            jsonData = self.queryConnectionPool.updateDoctorProfileBy(hospitalID, doctorID,name,degrees,visitFee,roomNo,maxPatientPerDay,specializationID,specialization)
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "missing required param"}
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def GetWeekLists(self,request):
        try:
            doctorID = request.POST.get('doctor_id',None)
            hospitalID = request.POST.get('hospital_id',None)
            if hospitalID !=None and doctorID !=None:
                jsonData = self.queryConnectionPool.getAllWeeksBy(hospitalID=hospitalID,doctorID=doctorID)
            else:
                jsonData = self.queryConnectionPool.getAllWeeks()
        except IntegrityError as e:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
        except:
            jsonData = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

        return HttpResponse(json.dumps(jsonData), content_type="application/json")

