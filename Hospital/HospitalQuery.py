import pymysql

from HealthBackendProject import Utility
from HealthBackendProject.StatusCode import StatusCode
from Doctor.models.DoctorData import DoctorData
from django.db import connection,IntegrityError
from datetime import datetime,timedelta
from Doctor.models.SpecializationData import SpecializationData
from django.core.exceptions import ObjectDoesNotExist
from .models.HospitalData import HospitalData
from HealthBackendProject.HashPassword import HashPassword
from .models.HospitalSpecializationData import HospitalSpecializationData
from .models.HospitalDoctorData import HospitalDoctorData
from .models.HospitalDoctorScheduleData import HospitalDoctorScheduleData
from .models.WeekData import WeekData
from .models.DoctorAppointmentData import DoctorAppointmentData
from HealthBackendProject.AppointmentStatus import AppointmentStatus
from .Services import HospitalService


class HospitalQuery:
    timeFormat = '%H:%M'
    timeFormatAmPm = '%H:%M %p'
    dateFormate = '%Y-%m-%d'

    def __init__(self, logger):
        self.logger = logger

    def cancelDoctorAppointment(self, doctorID, hospitalID, date):
        json_data = {}
        try:
            data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID,doctor_id=doctorID,
                                                        visit_date=datetime.strptime(date, self.dateFormate).date())
            for appointment in data:
                appointment.status = AppointmentStatus.CANCELLED.value
                appointment.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'selected appointments cancelled'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'no appointment found'}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

        return json_data

    def executeDoctorAppointment(self, doctorID, hospitalID, visitTime, visitDate,patientName,patientPhone,patientID):
        json_data = {}
        inputDate = datetime.strptime(visitDate, '%d-%m-%Y').date()
        # inputTime = datetime.strptime(visitTime, self.timeFormat).time()
        if inputDate >= datetime.now().date():
            visitorID = patientID if patientID > 0 else patientPhone
            serial = 0
            try:
                data = DoctorAppointmentData.objects.get(hospital_id=hospitalID,doctor_id=doctorID,visit_date=inputDate,patient_phone=patientPhone,patient_id=patientID)
                return {'code': StatusCode.HTTP_403_FORBIDDEN.value, 'message': 'already has a booking with this number for this date'}
            except ObjectDoesNotExist:
                serial = self.generateSerialNoBy(hospitalID, doctorID, inputDate)
                data = DoctorAppointmentData(hospital_id=hospitalID,doctor_id=doctorID,visit_date=inputDate,patient_phone=patientPhone,patient_id=patientID,patient_name=patientName,visit_time=visitTime,serial_no=serial)
                data.save()
                json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': "appointment successfull",'serialNo':serial}
            except:
                json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "some error occured"}
        else:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "cannot request for appointment using past date"}
        return json_data

    def generateSerialNoBy(self, hospitalID, doctorID, visitDate):
        serial = 0
        try:
            data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID,
                                                                   visit_date=visitDate).order_by("-serial_no")[0]
            serial = data.serial_no + 1
        except:
            return 1
        return serial

    def getAppointmentsby(self,hospitalID, doctorID, date):
        json_data = {}
        try:
            appointments = []
            if date is not None:
                data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID,
                                                                   visit_date=date).exclude(status=AppointmentStatus.CANCELLED.value).order_by("visit_date")
            else:
                data = DoctorAppointmentData.objects.filter(hospital_id=hospitalID, doctor_id=doctorID).exclude(status=AppointmentStatus.CANCELLED.value).order_by("visit_date")
            arrayLength = len(data)
            if arrayLength>0:
                selectedDate = data[0].visit_date
                appointmentData = []
            for index,item in enumerate(data):
                if item.visit_date != selectedDate:
                    appointments.append(
                        dict(date=selectedDate.strftime(self.dateFormate), appointments=appointmentData))
                    selectedDate = item.visit_date
                    appointmentData = []
                appointmentData.append(dict(id=item.id,
                                         time=item.visit_time,serial=item.serial_no,
                                         patient_phone=item.patient_phone,patient_name=item.patient_name,
                                         patient_id=item.patient_id))
                if index == arrayLength-1: #this condition is added
                    appointments.append(
                        dict(date=selectedDate.strftime(self.dateFormate), appointments=appointmentData))

            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success','data':appointments}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'no appointment found'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'somehting went wrong'}
        return json_data

    def removeDoctorScheduleFromHospital(self,doctorID, hospitalID, weekID):
        json_data = {}
        try:
            data = HospitalDoctorScheduleData.objects.get(doctor_id=doctorID,hospital_id=hospitalID,week_id=weekID)
            data.delete()
            json_data = {'code': StatusCode.HTTP_200_OK.value, "message": 'schedule day removed'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'unable to remove'}
        return json_data

    def updateDoctorScheduleForHospital(self,doctorID, hospitalID, weekID,startTime,endTime,isAvailable):
        json_data = {}
        try:
            data = HospitalDoctorScheduleData.objects.get(doctor_id=doctorID,hospital_id=hospitalID,week_id=weekID)
            if startTime is not None:
                data.visit_start_time = startTime
            if endTime is not None:
                data.visit_end_time = endTime
            if isAvailable is not None:
                data.is_available = isAvailable
            data.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, "message": 'schedule updated'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'schedule doesnt exists'}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}

        return json_data

    def executeAddDoctorScheduleDateToHospital(self, doctorID, hospitalID, weekID,startTime, endTime):
        json_data = {}
        try:
            data = HospitalDoctorScheduleData.objects.get(doctor_id=doctorID,hospital_id=hospitalID,week_id=weekID)
            json_data = {'code': StatusCode.HTTP_200_OK.value, "message": 'already exists'}
        except ObjectDoesNotExist:
            data = HospitalDoctorScheduleData(doctor_id=doctorID, hospital_id=hospitalID, week_id=weekID,is_available=1)
            if startTime is not None:
                data.visit_start_time = startTime
            if endTime is not None:
                data.visit_end_time = endTime
            data.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'schedule day added'}
        return json_data

    def getDoctorProfileBy(self, hospitalID,doctorID,request):
        json_data = {}
        try:
            info = HospitalDoctorData.objects.get(hospital_id=hospitalID,doctor_id=doctorID)
            availableDays = self.getAvailableWeekBy(doctorID=doctorID,hospitalID=hospitalID);
            scheduleDays = ' '.join(availableDays)
            data = {'name':info.doctor.name,'phone':info.doctor.phone,
                    'visit_fee':info.visit_fee if info.visit_fee is not None else '',
                    'days':scheduleDays,
                    'visit_start_time':info.visit_start_time if info.visit_start_time is not None else '',
                    'visit_end_time':info.visit_end_time if info.visit_end_time is not None else '',
                    'visit_start_day':info.visit_start_day if info.visit_start_day is not None else '',
                    'visit_end_day':info.visit_end_day if info.visit_end_day is not None else '',
                    'room_no':info.room_no if info.room_no is not None else '',
                    'degrees':info.doctor.degrees if info.doctor.degrees is not None else '',
                    'max_patient_per_day':info.max_patient_per_day if info.max_patient_per_day is not None else 0,
                    'photo':request.build_absolute_uri(info.doctor.photo.url) if info.doctor.photo else ''
                    }
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': data}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'no data found'}
        return json_data

    def updateDoctorProfileBy(self, hospitalID, doctorID,name,
                              degrees,visitFee,roomNo,
                              maxPatientPerDay,specializationID,
                              specialization,photo):
        json_data = {}
        try:
            doctorData = DoctorData.objects.get(id=doctorID)
            hospitalDoctor = HospitalDoctorData.objects.get(hospital_id=hospitalID,doctor_id=doctorID)
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
            if maxPatientPerDay is not None:
                hospitalDoctor.max_patient_per_day = maxPatientPerDay;
            if specializationID is not None and specializationID !='':
                doctorData.specialization = specializationID;
            doctorData.save()
            hospitalDoctor.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'successfully updated info'}
        except:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'user not found'}
        return json_data

    def getMaxAppointmentCount(self,doctorID,hospitalID)->int:
        maxCount = 0
        try:
            data = HospitalDoctorData.objects.get(doctor_id=doctorID,hospital_id=hospitalID)
            maxCount = data.max_patient_per_day
        except ObjectDoesNotExist:
            maxCount = 0
        return maxCount

    def getTotalAppointmentBy(self,hospitalID,doctorID=None,date=None)->int:
        try:
            return DoctorAppointmentData.objects.filter(hospital_id=hospitalID,doctor_id=doctorID,visit_date=date.strftime('%d-%m-%Y')).count
        except:
            return 0

    def isDoctorsScheduleAvailable(self, doctorID, hospitalID,date,maxAppointment)->bool:
        totalAppointment = self.getTotalAppointmentBy(hospitalID,doctorID,date)
        # self.logger.debug(f'total appointments ${totalAppointment}')
        # self.logger.debug(f'max appointments ${maxAppointment}')
        return maxAppointment>totalAppointment

    def generateAvailableSchedulesBy(self,doctorID,hospitalID,maxAppointment,filterDays,totalDays):
        schedule = []
        currentDate = datetime.utcnow() + timedelta(minutes=60 * 6)
        # totalDays indicate how many schedules we want to generate
        for i in range(totalDays):
            day = currentDate.strftime("%A").lower()
            # self.logger.debug(f'day ${day}')
            # self.logger.debug(f'filter days ${filterDays}')
            # check if the day is present in doctor's scheduled weekdays
            if day in filterDays:
                # self.logger.debug(f'day in filter days:......')
                # check whether the number of appointments in current date exceeds the doctor's max appointment number or not
                if self.isDoctorsScheduleAvailable(doctorID,hospitalID,currentDate,maxAppointment):
                    # self.logger.debug(f'converted date:......')
                    scheduleDate = str(currentDate.strftime('%d-%m-%Y'))
                    # self.logger.debug(f'schedule date ${scheduleDate}')
                    schedule.append({'date':scheduleDate,"day":day})
            currentDate = currentDate + timedelta(days=1) #
        return schedule

    def getDoctorsScheduleFromHospital(self,doctorID,hospitalID):
        weeks = self.getAvailableWeekBy(doctorID,hospitalID)
        # self.logger.debug(f'weeks ${weeks}')
        maxAppointment = self.getMaxAppointmentCount(doctorID,hospitalID)
        schedules = self.generateAvailableSchedulesBy(doctorID,hospitalID,maxAppointment,weeks,21)
        if len(schedules)>0:
            json_data =  {'code':StatusCode.HTTP_200_OK.value, 'message':'success', 'schedule':schedules}
        else:
            json_data = {'code': StatusCode.HTTP_403_FORBIDDEN.value, 'message': "no schedule found"}
        return json_data

    def getAvailableWeekBy(self,doctorID,hospitalID):
        week = []
        try:
            data = HospitalDoctorScheduleData.objects.filter(doctor_id=doctorID,hospital_id=hospitalID,is_available=1).order_by("week_id")
            for result in data:
                week.append(self.getWeekNameBy(result.week_id))
        except ObjectDoesNotExist:
            week = []
        return week

    def getWeekNameBy(self,id):
        week = ""
        try:
            data = WeekData.objects.get(id=id)
            week = data.name
        except ObjectDoesNotExist:
            week = ''
        return week

    def getAllWeeksBy(self,hospitalID,doctorID):
        json_data = {}
        try:
            weeks = []
            data = HospitalDoctorScheduleData.objects.filter(doctor_id=doctorID,hospital_id=hospitalID,is_available=1).order_by("week_id")
            if data.count()>0:
                for result in data:
                    startTime = "" if result.visit_start_time is None else result.visit_start_time
                    endTime = "" if result.visit_end_time is None else result.visit_end_time
                    weeks.append(dict(id=result.week_id, weekday=self.getWeekNameBy(result.week_id),start_time=startTime,end_time=endTime))
                json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': weeks}
            else:
                json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'no data found'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'no data found'}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
        return json_data

    def getAllWeeks(self):
        json_data = {}
        try:
            weeks = []
            data = WeekData.objects.all()
            for result in data:
                weeks.append(dict(id=result.id,weekday=result.name))
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': weeks}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': 'no data found'}
        return json_data

    def detachSpecializationFromHospital(self, specializationID, hospitalID):
        json_data = {}
        try:
            hospSp= HospitalSpecializationData.objects.get(hospital_id=hospitalID,specialization_id=specializationID)
            hospSp.delete()
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'removed successfully'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_403_FORBIDDEN.value, 'message': "no entry found"}
        except:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': "something went wrong"}

        return json_data

    def updateDoctorInfoForHospital(self, doctorID, hospitalID,phone,visitFee,startTime,endTime,startDay,endDay,roomNo,maxPatientPerDay):
        json_data = {}
        try:
            data = HospitalDoctorData.objects.get(doctor_id=doctorID,hospital_id=hospitalID)
            if phone!=None:
                data.phone = phone
            if visitFee!=None:
                data.visit_fee = visitFee
            if startTime != None:
                data.visit_start_time = startTime
            if endTime != None:
                data.visit_end_time = endTime
            if startDay != None:
                data.visit_start_day = startDay
            if endDay != None:
                data.visit_end_day = endDay
            if roomNo != None:
                data.room_no = roomNo
            if maxPatientPerDay != None:
                data.max_patient_per_day = maxPatientPerDay
            data.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, "message": 'successfully updated doctor info'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value,'message':'no data found'}
        return json_data

    def getHospitalList(self,request):
        try:
            data = HospitalData.objects.all()
            hospitals = []

            for item in data:
                hospitals.append(dict(name=item.name, phone=item.phone,
                                      id=item.id, address=item.address,icon= request.build_absolute_uri(item.logo.url) if item.logo else ''))
            return {'code': StatusCode.HTTP_200_OK.value, 'message': 'success', 'data': hospitals}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'no hospital found'}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'something went wrong'}
        return json_data

    def executeRegister(self,name,phone,password,licenseNo,logo):
        json_data = {}
        try:
            data = HospitalData.objects.get(license_no=licenseNo, phone=phone)
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value,
                         "message": 'account with this license_no or phone already exists'}
        except ObjectDoesNotExist:
            passwd = HashPassword.createPassword(password)
            data = HospitalData(name=name, password=passwd,license_no=licenseNo, phone=phone)
            if logo is not None:
                HospitalService.getProfileLogo(url=logo, data=data)
            data.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, "id": data.id}
        except:
            self.logger.debug('hospital object get/create exception')
            json_data = {'code': StatusCode.HTTP_403_FORBIDDEN.value, "message": 'Something went wrong'}

        return json_data

    # this method converts legacy user non-hashed password to hashed password
    def updateExistingNonHashedPasswordToHash(self, password, phone):
        json_data = {}
        try:
            data = HospitalData.objects.get(password=password, phone=phone)
            passwd = HashPassword.createPassword(password)
            data.password = passwd
            data.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, "message": 'password updated'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'user not found'}
        return json_data

    def doctorEntryOnHospitalList(self, doctorID, hospitalID):
        json_data = {}
        try:
            data = HospitalDoctorData.objects.get(hospital_id=hospitalID,doctor_id=doctorID)
            json_data = {'code':StatusCode.HTTP_403_FORBIDDEN.value, 'message':'doctor already exists'}
        except ObjectDoesNotExist:
            doctorData = DoctorData.objects.get(id=doctorID)
            data = HospitalDoctorData(hospital_id=hospitalID,doctor_id=doctorID,max_patient_per_day=8,phone=doctorData.phone)
            data.save()
            json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': "doctor added successfully"}
        except:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': "doctor no found"}

        return json_data

    def removeDoctorFromHospital(self, doctorID, hospitalID):
        json_data = {}
        try:
            data = HospitalDoctorData.objects.get(hospital_id=hospitalID,doctor_id=doctorID)
            data.delete()
            json_data = {'code':StatusCode.HTTP_200_OK.value, 'message':'doctor removed successfully'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, 'message': "no doctor found"}
        return json_data

    def login(self,request, phone, password):
        json_data = {}
        try:
            data = HospitalData.objects.get(phone=phone)
            json_data = {}
            if HashPassword.isValidPassword(password, data.password):
                json_data = {'code': StatusCode.HTTP_200_OK.value, "id": data.id, 'name': data.name,'icon':request.build_absolute_uri(data.logo.url) if data.logo else ''}
            else:
                json_data = {'code': StatusCode.HTTP_404_NOT_FOUND.value, "message": 'password doesnt match'}
        except ObjectDoesNotExist:
            json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'user not found'}
        except:
            json_data = {'code':StatusCode.HTTP_400_BAD_REQUEST, 'message':'Something Went Wrong'}
        return json_data

    def createWeekList(self):
        weeks = ['saturday','sunday','monday','tuesday','wednesday','thursday','friday']
        try:
            for week in weeks:
                data = WeekData(name=week)
                data.save()
        except:
            print('unable to create data')