from django.urls import path
from Hospital.Services import Hospital, API

urlpatterns = [
        path('api/doctorprofilestatus', API.GetDoctorProfileCompletionRatio, name=''),
        path('api/cancelappointment', API.CancelAppointment, name=''),
        path('api/createweeks', API.createWeekList, name=''),
        path('api/list', Hospital.HospitalList.as_view(), name='hospitallist'),
        path('api/weeklist', API.GetWeekLists, name=''),
        path('api/updateweek', API.UpdateWeek, name=''),
        path('api/doctorappointment', API.CreateDoctorAppointment, name=''),
        path('api/getappointments', API.GetDoctorAppointment, name=''),
        path('api/convertexistingnonhashedpasswordtohash', API.ConvertExistingNonHashedPasswordToHash, name=''),
        path('api/doctorschedules', API.DoctorSchedules, name=''),
        path('api/adddoctorscheduledatetohospital', API.AddDoctorScheduleDateToHospital, name=''),
        path('api/removedoctorschedulefromhospital', API.RemoveDoctorScheduleFromHospital, name=''),
        path('api/updatedoctorscheduleforhospital', API.UpdateDoctorScheduleForHospital, name=''),
        path('api/updatedoctorinfoforhospital', API.UpdateDoctorInfoInHospital, name=''),
        path('api/adddoctortohospital', API.AddDoctor, name=''),
        path('api/removedoctorfromhospital', API.removeDoctor, name=''),
        path('api/createspecialization', API.CreateSpecialization, name=''),
        path('api/addhospitalspecialization', API.AddSpecializationToHospital, name=''),
        path('api/removehospitalspecialization', API.RemoveSpecializationFromHospital, name=''),
        path('api/registerhospital', API.HospitalRegistration, name=''),
        path('api/specializationlist', API.SpecializationList, name=''),
        path('api/doctorProfileBy', API.DoctorProfile, name=''),
        path('api/login', API.Login, name=''),
        path('api/updateDoctorProfile', API.UpdateDoctorProfile, name='')
    ]
