from Hospital.Services import logger
from Hospital.models.HospitalData import HospitalData
from HealthBackendProject.StatusCode import StatusCode
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, IntegrityError
from HealthBackendProject import Utility
from Hospital.models.DoctorAppointmentData import DoctorAppointmentData
from Hospital.models.HospitalDoctorScheduleData import HospitalDoctorScheduleData
from Hospital.models.HospitalDoctorData import HospitalDoctorData
from Doctor.models.DoctorData import DoctorData

dateFormate = '%Y-%m-%d'

def doctor_profile_completion_ratio(hospital_id,doctor_id):
    rules = ['name','degree','schedule','max_patient']
    match_status = 0
    doctor_info = DoctorData.objects.get(id=doctor_id)
    if doctor_info is not  None:
        if doctor_info.name is not None:
            match_status +=1
        if doctor_info.degrees is not None:
            match_status += 1
    max_patient = HospitalDoctorData.objects.get(hospital_id=hospital_id,
                                                     doctor_id=doctor_id).max_patient_per_day
    if max_patient is not None and max_patient > 0:
        match_status += 1
    schedule = HospitalDoctorScheduleData.objects.filter(hospital_id=hospital_id,doctor_id=doctor_id)
    if len(schedule) > 0:
        match_status += 1
    return int((match_status/len(rules))*100)

def get_doctor_profile_completion(hospital_id,doctor_id):
    return {'code': StatusCode.HTTP_200_OK.value, 'completion_ratio': doctor_profile_completion_ratio(hospital_id=hospital_id,doctor_id=doctor_id)}

def getAppointmentsby(patientID):
    json_data = {}
    try:
        appointments = []
        data = DoctorAppointmentData.objects.filter(patient_id=patientID).order_by("visit_date")
        for index, item in enumerate(data):
            schedules = HospitalDoctorScheduleData.objects.filter(doctor_id=item.doctor.id,hospital_id=item.hospital.id)
            schedule = schedules[0]
            appointments.append(dict(id=item.id,
                                        date=item.visit_date.strftime(dateFormate), serial=item.serial_no,
                                        status=item.status,hospital=item.hospital.name,doctor=item.doctor.name,
                                        start_time=schedule.visit_start_time,end_time=schedule.visit_end_time,
                                        doctor_contact=item.doctor.phone,hospital_contact=item.hospital.phone
                                     ))
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
