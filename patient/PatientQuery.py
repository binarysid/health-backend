import pymysql
from django.db import connection
from .models.PatientData import PatientData
from django.core.exceptions import ObjectDoesNotExist
from HealthBackendProject.StatusCode import StatusCode
from HealthBackendProject.HashPassword import HashPassword

class PatientQuery:
    table = "patient"

    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    def register(self,name,phone,password,notification_reg_token):
        try:
            pat = PatientData.objects.get(phone=phone)
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'account with this number already exists'}
        except ObjectDoesNotExist:
            passwd = HashPassword.createPassword(password)
            patient = PatientData(name=name, phone=phone, password=passwd,notification_reg_token=notification_reg_token)
            patient.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, "id": patient.id}
        return json_data

    def login(self, phone, password,notification_reg_token):
        json_data = {}
        try:
            data = PatientData.objects.get(phone=phone)
            json_data = {}
            if HashPassword.isValidPassword(password, data.password):
                json_data = {'code': StatusCode.HTTP_200_OK.value, "id": data.id, 'name': data.name}
            else:
                json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'password doesnt match'}
            if data.notification_reg_token != notification_reg_token:
                data.notification_reg_token = notification_reg_token
                data.save()
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'user not found'}
        return json_data

    def removeUser(self,phone,password):
        json_data = {}
        try:
            data = PatientData.objects.get(phone=phone)
            if HashPassword.isValidPassword(password, data.password):
                data.delete()
                json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'user removed successfully'}
            else:
                json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'password doesnot match'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'user not found'}

        return json_data

