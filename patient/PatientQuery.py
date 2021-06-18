import pymysql
from django.db import connection
from .models.PatientData import PatientData
from django.core.exceptions import ObjectDoesNotExist
from HealthBackendProject.StatusCode import StatusCode
from HealthBackendProject.HashPassword import HashPassword
from HealthBackendProject.Service import ExceptionLogger
from HealthBackendProject import Utility

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
        except Exception as e:
            ExceptionLogger.track(e=e)
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

        return json_data

    def getPatientObj(self,status,data,request):
        responseObj = dict(code= status,message = 'success', id= data.id, name= data.name,
                             address=data.address,lat=data.lat,lng=data.lng,email=data.email)
        if data.photo:
            responseObj['photo'] = request.build_absolute_uri(data.photo.url)
        return responseObj

    def login(self,request, phone, password,notification_reg_token):
        json_data = {}
        try:
            data = PatientData.objects.get(phone=phone)
            json_data = {}
            if HashPassword.isValidPassword(password, data.password):
                json_data = self.getPatientObj(StatusCode.HTTP_200_OK.value,data=data,request=request)
            else:
                json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'password doesnt match'}
            if data.notification_reg_token != notification_reg_token:
                data.notification_reg_token = notification_reg_token
                data.save()
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'user not found'}
        except Exception as e:
            ExceptionLogger.track(e=e)
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

        return json_data

    def infoUpdate(self,name, id, password, email,
                   nid, address,lat,lng,photo,phone,request):
        json_data = {}
        try:
            data = PatientData.objects.get(id=id)
            if photo is not None:
                if data.photo:
                    Utility.removeFile(data.photo.path)
                data.photo = Utility.convertBase64ToImageFile(photo, id=id)
            if name != None:
                data.name = name
            if phone != None:
                data.phone = phone
            if password != None:
                data.password = HashPassword.createPassword(password)
            if email != None:
                data.email = email
            if nid != None:
                data.n_id = nid
            if address != None:
                data.address = address
            if lat != None:
                data.lat = float(lat)
            if lng != None:
                data.lng = float(lng)
            data.save()
            json_data = self.getPatientObj(status=StatusCode.HTTP_200_OK.value,data=data,request=request)
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'user not found'}
        except Exception as e:
            ExceptionLogger.track(e=e)
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

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
        except Exception as e:
            ExceptionLogger.track(e=e)
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

        return json_data

