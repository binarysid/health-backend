from .PatientQuery import PatientQuery
from django.db import IntegrityError
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from Hospital.Services import HospitalService

class API:
    queryConnectionPool = PatientQuery()

    @csrf_exempt
    def GetAppointments(self,request):
        id = int(request.POST.get('id',None))
        json_data = HospitalService.getAppointmentsby(patientID=id)
        return HttpResponse(json.dumps(json_data), content_type="application/json")

    @csrf_exempt
    def UserRegistration(self,request):
        name = request.POST.get('name',None)
        phone = request.POST.get('phone',None)
        password = request.POST.get('password',None)
        notification_reg_token = request.POST.get('notification_reg_token',None)
        json_data = self.queryConnectionPool.register(name,phone,password,notification_reg_token)
        return HttpResponse(json.dumps(json_data), content_type="application/json")

    @csrf_exempt
    def UserLogin(self,request):
        # version = request.headers['version']
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        notification_reg_token = request.POST.get('notification_reg_token',None)
        json_data = self.queryConnectionPool.login(request,phone, password, notification_reg_token)
        return HttpResponse(json.dumps(json_data), content_type="application/json")

    @csrf_exempt
    def RemovePatient(self,request):
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        json_data = self.queryConnectionPool.removeUser(phone, password)
        return HttpResponse(json.dumps(json_data), content_type="application/json")

    @csrf_exempt
    def UpdateInfo(self,request):
        id = int(request.POST.get('id', None))
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        nid = request.POST.get('nid', None)
        address = request.POST.get('address', None)
        lat = request.POST.get('lat', None)
        lng = request.POST.get('lng', None)
        photo = request.POST.get('photo', None)
        json_data = self.queryConnectionPool.infoUpdate(id=id,name=name,password=password,
                                                        email=email,address=address,
                                                        lat=lat,lng=lng,photo=photo,
                                                        nid=nid,phone=phone,request=request)
        return HttpResponse(json.dumps(json_data), content_type="application/json")
