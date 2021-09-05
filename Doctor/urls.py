from django.urls import path, include
from Doctor.Service.Doctor import Doctor
#from rest_framework import routers
from Doctor.Service import Api
# router = routers.DefaultRouter()
# router.register('api/doctorlist',Doctor,basename='doctorlist')
urlpatterns = [
        path('api/list', Doctor.as_view(
                {'get': 'list','post':'create','put':'update','delete':'destroy'},
        )),
        path('api/login', Api.DoctorLogin, name='doctorlogin'),
]