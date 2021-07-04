from django.urls import path, include
from . import views
from .API import API
from Hospital.Services import Hospital

api = API()
urlpatterns = [
        path('api/doctorprofilestatus', api.GetDoctorProfileCompletionRatio, name=''),
        path('api/infoupdate', api.UpdateInfo, name=''),
        path('api/cancelappointment', api.CancelAppointment, name=''),
        path('api/createweeks', api.createWeekList, name=''),
        path('api/hospitals', Hospital.HospitalList.as_view(), name=''),
        path('api/weeklist', api.GetWeekLists, name=''),
        path('api/updateweek', api.UpdateWeek, name=''),
        path('api/doctorappointment', api.CreateDoctorAppointment, name=''),
        path('api/getappointments', api.GetDoctorAppointment, name=''),
        path('api/convertexistingnonhashedpasswordtohash', api.ConvertExistingNonHashedPasswordToHash, name=''),
        path('api/doctorschedules', api.DoctorSchedules, name=''),
        path('api/adddoctorscheduledatetohospital', api.AddDoctorScheduleDateToHospital, name=''),
        path('api/removedoctorschedulefromhospital', api.RemoveDoctorScheduleFromHospital, name=''),
        path('api/updatedoctorscheduleforhospital', api.UpdateDoctorScheduleForHospital, name=''),
        path('api/updatedoctorinfoforhospital', api.UpdateDoctorInfoInHospital, name=''),
        path('api/adddoctortohospital', api.AddDoctor, name=''),
        path('api/removedoctorfromhospital', api.removeDoctor, name=''),
        path('api/createspecialization', api.CreateSpecialization, name=''),
        path('api/addhospitalspecialization', api.AddSpecializationToHospital, name=''),
        path('api/removehospitalspecialization', api.RemoveSpecializationFromHospital, name=''),
        path('api/registerhospital', api.HospitalRegistration, name=''),
        path('api/specializationlist', api.SpecializationList, name=''),
        path('api/doctorProfileBy', api.DoctorProfile, name=''),
        path('api/login', api.Login, name=''),
        path('api/updateDoctorProfile', api.UpdateDoctorProfile, name='')
    ]
