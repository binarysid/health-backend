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

class DoctorsQuery:

    def __init__(self,logger):
        self.logger = logger

    def getDoctorObj(self,data):
        responseObj = dict(name=data.name, phone=data.phone,
                               id=data.id)
        if data.address:
            responseObj['address'] = data.address
        responseObj['degrees'] = data.degrees if data.degrees is not None else ''
        if data.specialization:
            specData = SpecializationData.objects.get(id=data.specialization.id)
            responseObj['specialization'] = specData.specialization
        else:
            responseObj['specialization'] = ''
        return responseObj

    def getAllDoctorsBy(self, hospitalID, specializationID):
        json_data = {}
        try:
            doctors = []
            self.logger.debug('entered try')
            if hospitalID != None:
                filteredDoctor = HospitalDoctorData.objects.filter(hospital_id=hospitalID)
                self.logger.debug('doctor filtered')
                for doctor in filteredDoctor:
                    self.logger.debug('filter loop')
                    data = DoctorData.objects.get(id=doctor.doctor_id)
                    if specializationID is not None:
                        self.logger.debug(f'specialization not none ${specializationID}')
                        self.logger.debug(f'hospital id {hospitalID}')
                        self.logger.debug(f'doctor id {data.id}')
                        self.logger.debug(f'fake data specialization ${data.specialization_id}')
                        self.logger.debug(f'data specialization ${data.specialization.id}')
                        if data.specialization.id == specializationID:
                            self.logger.debug('specialization matches')
                            doctors.append(self.getDoctorObj(data))
                            self.logger.debug('doctor data appended')
                    else:
                        doctors.append(self.getDoctorObj(data))
            else:
                data = DoctorData.objects.all()
                for doctor in data:
                    doctors.append(self.getDoctorObj(doctor))
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': doctors}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'no doctor found'}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
        return json_data

    def infoUpdate(self,name, doctorID, password, email, nid, address,specializationID,degrees):
        json_data = {}
        try:
            data = DoctorData.objects.get(id=doctorID)
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

    def login(self, phone, password):
        json_data = {}
        try:
            data = DoctorData.objects.get(phone=phone)
            json_data = {}
            if HashPassword.isValidPassword(password, data.password):
                json_data = {'code': StatusCode.HTTP_200_OK.value, "id": data.id, 'name': data.name}
            else:
                json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'password doesnt match'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'user not found'}
        return json_data