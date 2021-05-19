from Hospital.Services import logger
from Hospital.models.HospitalData import HospitalData
from HealthBackendProject.StatusCode import StatusCode
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, IntegrityError
from HealthBackendProject import Utility
from Hospital.models.DoctorAppointmentData import DoctorAppointmentData

dateFormate = '%Y-%m-%d'
def getAppointmentsby(patientID):
    json_data = {}
    try:
        appointments = []
        data = DoctorAppointmentData.objects.filter(patient_id=patientID).order_by("visit_date")
        for index, item in enumerate(data):
            appointments.append(dict(id=item.id,
                                        date=item.visit_date.strftime(dateFormate), serial=item.serial_no,
                                        status=item.status,hospital=item.hospital.name,doctor=item.doctor.name))
        json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': appointments}

    except ObjectDoesNotExist:
        json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'no appointment found'}
    except:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'somehting went wrong'}
    return json_data

def infoUpdate(request,name, id, phone, password, email,
               address, lat, lng, logo):
    json_data = {}
    try:
        data = HospitalData.objects.get(id=id)
        if logo is not None:
            if data.logo:
                Utility.removeFile(data.logo.path)
            data.logo = Utility.convertBase64ToImageFile(logo, id=id)
        if name != None:
            data.name = name
        if password != None:
            data.password = HashPassword.createPassword(password)
        if email != None:
            data.email = email
        if phone != None:
            data.phone = phone
        if address != None:
            data.address = address
        if lat != None:
            lat = float(lat)
            data.lat = lat
        if lng != None:
            lng = float(lng)
            data.lng = lng
        data.save()
        json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'successfully updated info','data':getData(request=request,item=data)}
    except ObjectDoesNotExist:
        json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'user not found'}
    except:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
    return json_data

def getData(request,item):
    return dict(name=item.name, phone=item.phone,email=item.email,
         id=item.id, address=item.address,
         lat=item.lat, lng=item.lng,
         icon=request.build_absolute_uri(item.logo.url) if item.logo else '')
