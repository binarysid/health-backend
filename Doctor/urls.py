from django.urls import path, include
from . import views
from .API import API

api = API()
urlpatterns = [
        path('api/register', api.DoctorRegistration, name=''),
        path('api/login', api.DoctorLogin, name='doctorlogin'),
        path('api/infoupdate', api.DoctorInfoUpdate, name=''),
        path('api/degreeadd', api.DoctorDegreeAdd, name=''),
        path('api/list', api.DoctorList, name=''),
        path('api/remove', api.RemoveDoctor, name=''),
]