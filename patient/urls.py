from django.urls import path, include
from .API import API
api = API()

urlpatterns = [
        path('api/registerpatient', api.UserRegistration, name=''),
        path('api/loginpatient', api.UserLogin, name=''),
        path('api/removepatient', api.RemovePatient, name='')
]