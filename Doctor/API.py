from .DoctorsQuery import DoctorsQuery
from django.db import IntegrityError
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from HealthBackendProject.StatusCode import StatusCode
import logging


class API:
    def __init__(self):
        self.logger = self.getLogHandler()
        self.queryConnectionPool = DoctorsQuery(logger=self.logger)

    def getLogHandler(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s]: %(levelname)s: %(name)s: %(funcName)s: %(filename)s: line no- %(lineno)s : %(message)s')
        fileHandler = logging.FileHandler('doctor.log')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        return logger

    @csrf_exempt
    def DoctorList(self,request):
        specializationID = request.POST.get('specialization_id',None)
        doctorName = request.POST.get('doctor_name', None)
        if specializationID is not None:
            specializationID = int(specializationID)
        specialization = request.POST.get('specialization',None)
        hospitalID = request.POST.get('hospital_id',None)
        if hospitalID is not None:
            hospitalID = int(hospitalID)
        jsonData = self.queryConnectionPool.getAllDoctorsBy(hospitalID=hospitalID,specializationID=specializationID,request=request)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def DoctorDegreeAdd(self,request):
        degree = request.POST.get('degree',None)
        doctorID = request.POST.get('doctor_id',None)
        jsonData = self.queryConnectionPool.executeDegreeAdd(degree, doctorID)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def DoctorInfoUpdate(self,request):
        doctorID = int(request.POST.get('doctor_id', None))
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        nid = request.POST.get('nid', None)
        address = request.POST.get('address', None)
        degrees = request.POST.get('degrees', None)
        specializationID = request.POST.get('specialization_id', None)
        specializationID = None if specializationID == None else int(specializationID)
        photo = request.POST.get('photo', None)
        jsonData = self.queryConnectionPool.infoUpdate(name=name, doctorID=doctorID, password=password, email=email,
                                                       nid=nid, address=address,
                                                        specializationID=specializationID,
                                                       degrees=degrees,photo=photo)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def DoctorRegistration(self,request):
        self.logger.debug('reg api initiated')
        name = request.POST.get('name', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        registrationNo = request.POST.get('reg_no', None)
        hospitalID = request.POST.get('hospital_id', None)
        specializationID = request.POST.get('specialization_id', None)
        if specializationID is not None:
            specializationID = int(specializationID)
        if hospitalID is not None:
            hospitalID = int(hospitalID)
        jsonData = self.queryConnectionPool.register(name, phone, password, registrationNo, hospitalID,specializationID=specializationID)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def DoctorLogin(self,request):
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        jsonData = self.queryConnectionPool.login(phone=phone, password=password,request=request)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def RemoveDoctor(self,request):
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        jsonData = self.queryConnectionPool.executeRemoveUser(phone, password)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")
