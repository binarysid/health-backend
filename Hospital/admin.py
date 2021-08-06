from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib import messages
from Hospital.models.HospitalData import HospitalData
from Hospital.models.DoctorAppointmentData import DoctorAppointmentData
from Hospital.models.HospitalDoctorData import HospitalDoctorData
from Hospital.models.HospitalDoctorScheduleData import HospitalDoctorScheduleData
from Hospital.models.HospitalSpecializationData import HospitalSpecializationData
from Hospital.models.WeekData import WeekData
from Doctor.models.DoctorData import DoctorData
from Doctor.models.SpecializationData import SpecializationData
from patient.models.PatientData import PatientData

admin.site.site_header = 'GanymedeCube'


class StateAdmin(admin.ModelAdmin):
    list_display = ('name','created_on','updated_on')

    # def make_active(modeladmin, request, queryset):
    #     queryset.update(is_active=1) # is_active is the db field name
    #     messages.success(request, "Selected Record(s) Marked as Active Successfully !!")
    # # add dropdpwn action
    # admin.site.add_action(make_active, "Make Active")

# Register your models here.
admin.site.register(HospitalData)
admin.site.register(DoctorAppointmentData)
admin.site.register(HospitalDoctorData)
admin.site.register(HospitalDoctorScheduleData)
admin.site.register(HospitalSpecializationData)
admin.site.register(WeekData)
admin.site.register(PatientData)
admin.site.register(DoctorData,StateAdmin)
admin.site.register(SpecializationData)

admin.site.unregister(Group)