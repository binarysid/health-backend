from Hospital.Services import logger
from Hospital.models.HospitalData import HospitalData
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, IntegrityError
from HealthBackendProject import Utility
from Hospital.models.DoctorAppointmentData import DoctorAppointmentData
from Hospital.models.HospitalDoctorScheduleData import HospitalDoctorScheduleData
from Hospital.models.HospitalDoctorData import HospitalDoctorData
from HealthBackendProject.AppointmentStatus import AppointmentStatus
from Doctor.models.DoctorData import DoctorData
from HealthBackendProject.Service import ExceptionLogger
from datetime import datetime,timedelta
from Doctor.models.SpecializationData import SpecializationData
from HealthBackendProject.HashPassword import HashPassword
from ..models.HospitalSpecializationData import HospitalSpecializationData
from ..models.WeekData import WeekData
from HealthBackendProject.Service import PushNotification
from patient.models.PatientData import PatientData
from rest_framework import status


def cancelDoctorAppointment(doctorID, hospitalID, date):
    json_data = {}
    try:
        data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID,
                                                    visit_date=datetime.strptime(date, Utility.date_format_DMY).date())
        for appointment in data:
            appointment.status = AppointmentStatus.CANCELLED
            appointment.save()
        PushNotification.send_appntment_cancel_notification(appointment_info=data)
        json_data = {'code': status.HTTP_200_OK, 'message': 'selected appointments cancelled'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'no appointment found'}
    except Exception as e:
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'something went wrong'}
        ExceptionLogger.track(e=e)
    return json_data

def serial_no_is_valid(serial,doctor_id, hospital_id, visit_date):
    try:
        return serial <= getMaxAppointmentCountBy(doctor_id=doctor_id,
                                              hospital_id=hospital_id,
                                              date=visit_date,format=Utility.date_format_DMY)
    except Exception as e:
        ExceptionLogger.log(e)
def get_appointment_visit_time(doctor_id,hospital_id,serial,visit_date,date_format,time_format):
    data = HospitalDoctorData.objects.get(doctor_id=doctor_id, hospital_id=hospital_id)
    week_id = WeekData.objects.get(name=Utility.get_day_from(date=visit_date,format=date_format)).id
    schedule = HospitalDoctorScheduleData.objects.get(doctor_id=doctor_id,hospital_id=hospital_id,week_id=week_id)
    time_range = Utility.getTimeRange(start_time=schedule.visit_start_time,
                                      end_time=schedule.visit_end_time,
                                      interval=data.time_spent_per_patient,format=time_format)
    #if(len(time_range)>serial):
    return time_range[serial-1]
    #return None

def executeDoctorAppointment(doctorID, hospitalID, visitDate, patientName, patientPhone, patientID):
    json_data = {}
    inputDate = datetime.strptime(visitDate, Utility.date_format_DMY).date()
    if inputDate >= datetime.now().date():
        serial = 0
        try:
            data = DoctorAppointmentData.objects.get(hospital_id=hospitalID, doctor_id=doctorID, visit_date=inputDate,
                                                     patient_phone=patientPhone, patient_id=patientID)
            return {'code': status.HTTP_403_FORBIDDEN,
                    'message': 'already has a booking with this number for this date'}
        except ObjectDoesNotExist:
            serial = generateSerialNoBy(hospitalID, doctorID, inputDate)
            if serial_no_is_valid(serial=serial,doctor_id=doctorID, hospital_id=hospitalID, visit_date=inputDate):
                patient = None
                if patientID != None:
                    patient = PatientData.objects.get(id=patientID)
                time = get_appointment_visit_time(hospital_id=hospitalID,
                                                  doctor_id=doctorID,
                                                 serial=serial,
                                                 visit_date=inputDate,
                                                 date_format=Utility.date_format_DMY,
                                                 time_format=Utility.time_format_12_am_pm)
                if time is None:
                    return {'code': status.HTTP_403_FORBIDDEN,
                            'message': 'this doctor reached booking limit for this date. plz try booking another date'}

                data = DoctorAppointmentData(hospital_id=hospitalID, doctor_id=doctorID, visit_date=inputDate,
                                             patient_phone=patientPhone, patient=patient,
                                             patient_name=patientName, visit_time=time,
                                             serial_no=serial)
                data.save()
                json_data = {'code': status.HTTP_200_OK, 'message': "appointment successfull", 'serialNo': serial, 'time':time}
            else:
                return {'code': status.HTTP_403_FORBIDDEN,
                    'message': 'this doctor reached booking limit for this date. plz try booking another date'}
        except Exception as e:
            json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': "some error occured"}
            ExceptionLogger.track(e=e)
    else:
        json_data = {'code': status.HTTP_400_BAD_REQUEST,
                     'message': "cannot request for appointment using past date"}
    return json_data

# def generateEstimatedVisitTime(serial,start_time,end_time):

def generateSerialNoBy(hospitalID, doctorID, visitDate):
    serial = 0
    try:
        data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID,
                                                    visit_date=visitDate).order_by("-serial_no")[0]
        serial = data.serial_no + 1
    except:
        return 1
    return serial

def getAppointments(hospitalID, doctorID, date):
    json_data = {}
    try:
        appointments = []
        if date is not None:
            data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID,
                                                        visit_date=date).exclude(
                status=AppointmentStatus.CANCELLED.value).order_by("visit_date")
        else:
            data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID).exclude(
                status=AppointmentStatus.CANCELLED.value).order_by("visit_date")
        arrayLength = len(data)
        if arrayLength > 0:
            selectedDate = data[0].visit_date
            appointmentData = []
        for index, item in enumerate(data):
            if item.visit_date != selectedDate:
                appointments.append(
                    dict(date=selectedDate.strftime(Utility.date_format_DMY), appointments=appointmentData))
                selectedDate = item.visit_date
                appointmentData = []
            appointmentData.append(dict(id=item.id,
                                        time=item.visit_time, serial=item.serial_no,
                                        patient_phone=item.patient_phone, patient_name=item.patient_name,
                                        patient_id=item.patient_id))
            if index == arrayLength - 1:  # this condition is added
                appointments.append(
                    dict(date=selectedDate.strftime(Utility.dateFormate), appointments=appointmentData))

        json_data = {'code': status.HTTP_200_OK, 'message': 'success', 'data': appointments}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'no appointment found'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'somehting went wrong'}
    return json_data


def removeDoctorScheduleFromHospital(doctorID, hospitalID, weekID):
    json_data = {}
    try:
        data = HospitalDoctorScheduleData.objects.get(doctor_id=doctorID, hospital_id=hospitalID, week_id=weekID)
        data.delete()
        json_data = {'code': status.HTTP_200_OK, "message": 'schedule day removed'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'unable to remove'}
    except Exception as e:
        ExceptionLogger.track(e=e)
    return json_data


def updateDoctorScheduleForHospital(doctorID, hospitalID, weekID, startTime, endTime, isAvailable):
    json_data = {}
    try:
        data = HospitalDoctorScheduleData.objects.get(doctor_id=doctorID, hospital_id=hospitalID, week_id=weekID)
        if startTime is not None:
            data.visit_start_time = startTime
        if endTime is not None:
            data.visit_end_time = endTime
        if isAvailable is not None:
            data.is_available = isAvailable
        data.save()
        json_data = {'code': status.HTTP_200_OK, "message": 'schedule updated'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'schedule doesnt exists'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'something went wrong'}

    return json_data


def executeAddDoctorScheduleDateToHospital(doctorID, hospitalID, weekID, startTime, endTime):
    json_data = {}
    try:
        data = HospitalDoctorScheduleData.objects.get(doctor_id=doctorID, hospital_id=hospitalID, week_id=weekID)
        json_data = {'code': status.HTTP_200_OK, "message": 'already exists'}
    except ObjectDoesNotExist:
        data = HospitalDoctorScheduleData(doctor_id=doctorID, hospital_id=hospitalID, week_id=weekID, is_available=1)
        if startTime is not None:
            data.visit_start_time = startTime
        if endTime is not None:
            data.visit_end_time = endTime
        data.save()
        json_data = {'code': status.HTTP_200_OK, 'message': 'schedule day added'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'something went wrong'}

    return json_data


def getDoctorProfileBy(hospitalID, doctorID, request):
    json_data = {}
    try:
        info = HospitalDoctorData.objects.get(hospital_id=hospitalID, doctor_id=doctorID)
        specialization = info.doctor.specialization.specialization
        availableDays = getAvailableWeekBy(doctorID=doctorID, hospitalID=hospitalID);
        scheduleDays = ' '.join(availableDays)
        data = {'name': info.doctor.name, 'phone': info.doctor.phone,
                'visit_fee': info.visit_fee if info.visit_fee is not None else '',
                'days': scheduleDays,
                'visit_start_time': info.visit_start_time if info.visit_start_time is not None else '',
                'visit_end_time': info.visit_end_time if info.visit_end_time is not None else '',
                'visit_start_day': info.visit_start_day if info.visit_start_day is not None else '',
                'visit_end_day': info.visit_end_day if info.visit_end_day is not None else '',
                'room_no': info.room_no if info.room_no is not None else '',
                'degrees': info.doctor.degrees if info.doctor.degrees is not None else '',
                'photo': request.build_absolute_uri(info.doctor.photo.url) if info.doctor.photo else '',
                'specialization': specialization if specialization else ''
                }
        json_data = {'code': status.HTTP_200_OK, 'message': 'success', 'data': data}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'no data found'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'something went wrong'}

    return json_data


def updateDoctorProfileBy(hospitalID, doctorID, name,
                          degrees, visitFee, roomNo,
                          maxPatientPerDay, specializationID,
                          specialization, photo):
    json_data = {}
    try:
        doctorData = DoctorData.objects.get(id=doctorID)
        hospitalDoctor = HospitalDoctorData.objects.get(hospital_id=hospitalID, doctor_id=doctorID)
        if photo is not None:
            if doctorData.photo:
                Utility.removeFile(doctorData.photo.path)
            doctorData.photo = Utility.convertBase64ToImageFile(photo, id=doctorID)

        if name is not None and name != '':
            doctorData.name = name;
        if degrees is not None and degrees != '':
            doctorData.degrees = degrees;
        if visitFee is not None and visitFee != '':
            hospitalDoctor.visit_fee = visitFee;
        if roomNo is not None and roomNo != '':
            hospitalDoctor.room_no = roomNo;
        if specializationID is not None and specializationID != '':
            doctorData.specialization = specializationID;
        doctorData.save()
        hospitalDoctor.save()
        json_data = {'code': status.HTTP_200_OK, 'message': 'successfully updated info'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'user not found'}
    return json_data


def getMaxAppointmentCountBy(doctor_id,hospital_id,date,format):
    data = HospitalDoctorData.objects.get(doctor_id=doctor_id, hospital_id=hospital_id)
    week_id = WeekData.objects.get(name=Utility.get_day_from(date=date,format=format)).id
    schedule = HospitalDoctorScheduleData.objects.get(doctor_id=doctor_id,hospital_id=hospital_id,week_id=week_id)
    timeDiff = Utility.getTimeDiff(start_time=schedule.visit_start_time,
                                   end_time=schedule.visit_end_time,
                                   format=Utility.time_format_12_am_pm)
    return int(timeDiff/data.time_spent_per_patient)

def getTotalAppointmentBy(hospitalID, doctorID=None, date=None) -> int:
    try:
        return DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID,
                                                    visit_date=date.strftime(Utility.date_format_DMY)).count
    except:
        return 0


def isDoctorsScheduleAvailable(doctorID, hospitalID, date, maxAppointment) -> bool:
    totalAppointment = getTotalAppointmentBy(hospitalID, doctorID, date)
    # logger.debug(f'total appointments ${totalAppointment}')
    # logger.debug(f'max appointments ${maxAppointment}')
    return maxAppointment > totalAppointment


def generateAvailableSchedulesBy(doctorID, hospitalID, filterDays, totalDays):
    schedule = []
    try:
        currentDate = datetime.utcnow() + timedelta(minutes=60 * 6)
        # totalDays indicate how many schedules we want to generate
        for i in range(totalDays):
            day = currentDate.strftime("%A").lower()
            # logger.debug(f'day ${day}')
            # logger.debug(f'filter days ${filterDays}')
            # check if the day is present in doctor's scheduled weekdays
            if day in filterDays:
                # logger.debug(f'day in filter days:......')
                # check whether the number of appointments in current date exceeds the doctor's max appointment number or not
                if isDoctorsScheduleAvailable(doctorID, hospitalID, currentDate, getMaxAppointmentCountBy(doctor_id=doctorID,
                                                                                                          hospital_id=hospitalID,date=currentDate,format=Utility.date_format_DMY)):
                    # logger.debug(f'converted date:......')
                    scheduleDate = str(currentDate.strftime(Utility.date_format_DMY))
                    # logger.debug(f'schedule date ${scheduleDate}')
                    schedule.append({'date': scheduleDate, "day": day})
            currentDate = currentDate + timedelta(days=1)  #
    except Exception as e:
        ExceptionLogger.track(e=e)
    return schedule


def getDoctorsScheduleFromHospital(doctorID, hospitalID):
    weeks = getAvailableWeekBy(doctorID, hospitalID)
    # logger.debug(f'weeks ${weeks}')
    schedules = generateAvailableSchedulesBy(doctorID, hospitalID, weeks, 21)
    if len(schedules) > 0:
        json_data = {'code': status.HTTP_200_OK, 'message': 'success', 'schedule': schedules}
    else:
        json_data = {'code': status.HTTP_403_FORBIDDEN, 'message': "no schedule found"}
    return json_data


def getAvailableWeekBy(doctorID, hospitalID):
    week = []
    try:
        data = HospitalDoctorScheduleData.objects.filter(doctor_id=doctorID, hospital_id=hospitalID,
                                                         is_available=1).order_by("week_id")
        for result in data:
            week.append(getWeekNameBy(result.week_id))
    except ObjectDoesNotExist:
        week = []
    return week


def getWeekNameBy(id):
    week = ""
    try:
        data = WeekData.objects.get(id=id)
        week = data.name
    except ObjectDoesNotExist:
        week = ''
    return week


def getAllWeeksBy(hospitalID, doctorID):
    json_data = {}
    try:
        weeks = []
        data = HospitalDoctorScheduleData.objects.filter(doctor_id=doctorID, hospital_id=hospitalID,
                                                         is_available=1).order_by("week_id")
        if data.count() > 0:
            for result in data:
                startTime = "" if result.visit_start_time is None else result.visit_start_time
                endTime = "" if result.visit_end_time is None else result.visit_end_time
                weeks.append(dict(id=result.week_id, weekday=getWeekNameBy(result.week_id), start_time=startTime,
                                  end_time=endTime))
            json_data = {'code': status.HTTP_200_OK, 'message': 'success', 'data': weeks}
        else:
            json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'no data found'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'no data found'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'something went wrong'}
    return json_data


def getAllWeeks():
    json_data = {}
    try:
        weeks = []
        data = WeekData.objects.all()
        for result in data:
            weeks.append(dict(id=result.id, weekday=result.name))
        json_data = {'code': status.HTTP_200_OK, 'message': 'success', 'data': weeks}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'no data found'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'something went wrong'}

    return json_data


def detachSpecializationFromHospital(specializationID, hospitalID):
    json_data = {}
    try:
        hospSp = HospitalSpecializationData.objects.get(hospital_id=hospitalID, specialization_id=specializationID)
        hospSp.delete()
        json_data = {'code': status.HTTP_200_OK, 'message': 'removed successfully'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_403_FORBIDDEN, 'message': "no entry found"}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': "something went wrong"}

    return json_data


# this method converts legacy user non-hashed password to hashed password
def updateExistingNonHashedPasswordToHash(password, phone):
    json_data = {}
    try:
        data = HospitalData.objects.get(password=password, phone=phone)
        passwd = HashPassword.createPassword(password)
        data.password = passwd
        data.save()
        json_data = {'code': status.HTTP_200_OK, "message": 'password updated'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, "message": 'user not found'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, "message": 'something went wrong'}

    return json_data


def doctorEntryOnHospitalList(doctorID, hospitalID):
    json_data = {}
    try:
        data = HospitalDoctorData.objects.get(hospital_id=hospitalID, doctor_id=doctorID)
        json_data = {'code': status.HTTP_403_FORBIDDEN, 'message': 'doctor already exists'}
    except ObjectDoesNotExist:
        doctorData = DoctorData.objects.get(id=doctorID)
        hosp_doctor_data = HospitalDoctorData(hospital_id=hospitalID, doctor=doctorData, phone=doctorData.phone)
        hosp_doctor_data.save()
        json_data = {'code': status.HTTP_200_OK, 'message': "doctor added successfully"}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': "doctor no found"}

    return json_data


def removeDoctorFromHospital(doctorID, hospitalID):
    json_data = {}
    try:
        data = HospitalDoctorData.objects.get(hospital_id=hospitalID, doctor_id=doctorID)
        data.delete()
        json_data = {'code': status.HTTP_200_OK, 'message': 'doctor removed successfully'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': "no doctor found"}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': "something went wrong"}

    return json_data


def login(request, phone, password):
    json_data = {}
    try:
        data = HospitalData.objects.get(phone=phone)
        json_data = {}
        if HashPassword.isValidPassword(password, data.password):
            json_data = {'code': status.HTTP_200_OK, "id": data.id, 'name': data.name,
                         'icon': request.build_absolute_uri(data.logo.url) if data.logo else '',
                         'data': getData(request=request, item=data)}
        else:
            json_data = {'code': status.HTTP_404_NOT_FOUND, "message": 'password doesnt match'}
    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'user not found'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'Something Went Wrong'}
    return json_data


def createWeekList():
    weeks = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    try:
        for week in weeks:
            data = WeekData(name=week)
            data.save()
    except:
        print('unable to create data')


def doctor_profile_completion_ratio(hospital_id,doctor_id):
    rules = ['name','degree','schedule','max_patient']
    match_status = 0
    doctor_info = DoctorData.objects.get(id=doctor_id)
    if doctor_info is not  None:
        if doctor_info.name is not None:
            match_status +=1
        if doctor_info.degrees is not None:
            match_status += 1
    time_spent_per_patient = HospitalDoctorData.objects.get(hospital_id=hospital_id,
                                                     doctor_id=doctor_id).time_spent_per_patient
    if time_spent_per_patient is not None and time_spent_per_patient > 0:
        match_status += 1
    schedule = HospitalDoctorScheduleData.objects.filter(hospital_id=hospital_id,doctor_id=doctor_id)
    if len(schedule) > 0:
        match_status += 1
    ratio = int((match_status/len(rules))*100)
    return ratio

def get_doctor_profile_completion(hospital_id,doctor_id):
    return {'code': status.HTTP_200_OK, 'completion_ratio': doctor_profile_completion_ratio(hospital_id=hospital_id,doctor_id=doctor_id)}

def getAppointmentsby(patientID):
    json_data = {}
    try:
        appointments = []
        data = DoctorAppointmentData.objects.filter(patient_id=patientID).order_by("visit_date")
        for index, item in enumerate(data):
            schedules = HospitalDoctorScheduleData.objects.filter(doctor_id=item.doctor_id,hospital_id=item.hospital_id)
            schedule = schedules[0]
            specialization = item.doctor.specialization.specialization
            appointments.append(dict(id=item.id,
                                        date=item.visit_date.strftime(Utility.dateFormate), serial=item.serial_no,
                                        status=item.status,hospital=item.hospital.name,doctor=item.doctor.name,
                                        start_time=schedule.visit_start_time,end_time=schedule.visit_end_time,
                                        doctor_contact=item.doctor.phone,hospital_contact=item.hospital.phone,specialization=specialization
                                     ))
        json_data = {'code': status.HTTP_200_OK, 'message': 'success', 'data': appointments}

    except ObjectDoesNotExist:
        json_data = {'code': status.HTTP_404_NOT_FOUND, 'message': 'no appointment found'}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': 'somehting went wrong'}
    return json_data


def getData(request,item):
    return dict(name=item.name, phone=item.phone,email=item.email,
         id=item.id, address=item.address,
         lat=item.lat, lng=item.lng,
         icon=request.build_absolute_uri(item.logo.url) if item.logo else '')


def doctorEntryOnHospitalList(doctorID, hospitalID):
    json_data = {}
    try:
        data = HospitalDoctorData.objects.get(hospital_id=hospitalID, doctor_id=doctorID)
        json_data = {'code': status.HTTP_403_FORBIDDEN, 'message': 'doctor already exists'}
    except ObjectDoesNotExist:
        doctorData = DoctorData.objects.get(id=doctorID)
        hosp_doctor_data = HospitalDoctorData(hospital_id=hospitalID, doctor=doctorData, phone=doctorData.phone)
        hosp_doctor_data.save()
        json_data = {'code': status.HTTP_200_OK, 'message': "doctor added successfully"}
    except Exception as e:
        ExceptionLogger.track(e=e)
        json_data = {'code': status.HTTP_400_BAD_REQUEST, 'message': "doctor no found"}

    return json_data