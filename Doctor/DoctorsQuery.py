import uuid
import binascii
import json
import pymysql
from django.db import connection
from HealthBackendProject.StatusCode import StatusCode
from HealthBackendProject.HashPassword import HashPassword
from .models.DoctorData import DoctorData
from .models.SpecializationData import SpecializationData
from django.core.exceptions import ObjectDoesNotExist
from Hospital.models.HospitalDoctorData import HospitalDoctorData
from Hospital.HospitalQuery import HospitalQuery
from HealthBackendProject import Utility

class DoctorsQuery:

    def __init__(self,logger):
        self.logger = logger

    def getDoctorObj(self,data,request):
        responseObj = dict(name=data.name, phone=data.phone,
                               id=data.id)
        if data.photo:
            responseObj['photo'] = request.build_absolute_uri(data.photo.url)
        if data.address:
            responseObj['address'] = data.address
        responseObj['degrees'] = data.degrees if data.degrees is not None else ''
        if data.specialization:
            specData = SpecializationData.objects.get(id=data.specialization.id)
            responseObj['specialization'] = specData.specialization
        else:
            responseObj['specialization'] = ''
        return responseObj

    def getAllDoctorsBy(self, hospitalID, specializationID,request):
        json_data = {}
        try:
            doctors = []
            self.logger.debug('entered try')
            if hospitalID != None:
                filteredDoctor = HospitalDoctorData.objects.filter(hospital_id=hospitalID)
                for doctor in filteredDoctor:
                    if specializationID is not None:
                        data = self.getDoctorBySpecialization(doctorID=doctor.doctor_id,specializationID=specializationID)
                        if data is None:
                            continue
                    else:
                        data = DoctorData.objects.get(id=doctor.doctor_id)
                    doctors.append(self.getDoctorObj(data,request))
            else:
                data = DoctorData.objects.all()
                for doctor in data:
                    doctors.append(self.getDoctorObj(doctor,request))
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': doctors}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'no doctor found'}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
        return json_data

    def getDoctorBySpecialization(self,doctorID,specializationID):
        try:
            return DoctorData.objects.get(id=doctorID,specialization_id=specializationID)
        except:
            return None

    def infoUpdate(self,name, doctorID, password, email,
                   nid, address,specializationID,degrees,photo):
        json_data = {}
        try:
            data = DoctorData.objects.get(id=doctorID)
            if photo is not None:
                self.logger.debug(f'photo base64: {photo}')
                if data.photo:
                    Utility.removeFile(data.photo.path)
                data.photo = Utility.convertBase64ToImageFile(photo, id=doctorID)
            if name != None:
                data.name = name
            if password != None:
                data.password = HashPassword.createPassword(password)
            if email != None:
                data.email = email
            if nid != None:
                data.nid = nid
            if address != None:
                data.address = address
            if specializationID != None:
                data.specialization = SpecializationData.objects.get(id=specializationID)
            if degrees != None:
                data.degrees = degrees
            data.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'successfully updated info'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'user not found'}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
        return json_data

    def getSpecializationObj(self,id):
        try:
            return SpecializationData.objects.get(id=id)
        except:
            return None

    def register(self, name, phone, password, regNo, hospitalID,specializationID):
        json_data = {}
        hospitalAPI = HospitalQuery(self.logger)
        try:
            data = DoctorData.objects.get(reg_no=regNo,phone=phone)
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'account with this reg_no or phone already exists'}
        except ObjectDoesNotExist:
            passwd = HashPassword.createPassword(password)
            data = DoctorData(name=name,reg_no=regNo,password=passwd,phone=phone,specialization=self.getSpecializationObj(specializationID))
            data.save()
            if hospitalID is not None:
                response = self.addDoctorToHospital(hospitalID=hospitalID,doctorID=data.id,hospitalAPIObj=hospitalAPI)
                if response['code'] == StatusCode.HTTP_200_OK.value: # if this api is requested with hospitalID, then it should be from hospital app. so the message should be whether it's successfully attached the doctor to hospital
                    json_data = response
                    json_data["id"] = data.id
                else:
                    json_data = {'code': StatusCode.HTTP_200_OK.value, "id": data.id,'message':'successfully registered'}
            else:
                json_data = {'code': StatusCode.HTTP_200_OK.value, "id": data.id,'message':'successfully registered'}
        return json_data

    def addDoctorToHospital(self,hospitalID,doctorID,hospitalAPIObj):
        json_data = {}
        try:
            json_data = hospitalAPIObj.doctorEntryOnHospitalList(doctorID=doctorID, hospitalID=hospitalID)
        except:
            json_data = {'code':StatusCode.HTTP_404_NOT_FOUND.value,'message':'unable to add doctor to hospital'}
        return json_data

    def login(self, phone, password,request):
        json_data = {}
        try:
            data = DoctorData.objects.get(phone=phone)
            json_data = {}
            if HashPassword.isValidPassword(password, data.password):
                json_data = {'code': StatusCode.HTTP_200_OK.value, "id": data.id, 'name': data.name,'photo':request.build_absolute_uri(data.photo.url) if data.photo else ''}
            else:
                json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'password doesnt match'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'user not found'}
        return json_data