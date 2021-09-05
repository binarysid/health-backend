from rest_framework.decorators import api_view
from Doctor.Service import DoctorService


@api_view(['POST',])
def DoctorLogin(request):
    phone = request.POST.get('phone', None)
    password = request.POST.get('password', None)
    return DoctorService.login(phone=phone, password=password, request=request)
