from .PatientQuery import PatientQuery
from django.db import IntegrityError
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

class API:
    queryConnectionPool = PatientQuery()

    @csrf_exempt
    def UserRegistration(self,request):
        name = request.POST.get('name',None)
        phone = request.POST.get('phone',None)
        password = request.POST.get('password',None)
        notification_reg_token = request.POST.get('notification_reg_token',None)
        jsonData = self.queryConnectionPool.register(name,phone,password,notification_reg_token)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def UserLogin(self,request):
        # version = request.headers['version']
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        notification_reg_token = request.POST.get('notification_reg_token',None)
        jsonData = self.queryConnectionPool.login(phone, password, notification_reg_token)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")

    @csrf_exempt
    def RemovePatient(self,request):
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        jsonData = self.queryConnectionPool.removeUser(phone, password)
        return HttpResponse(json.dumps(jsonData), content_type="application/json")
