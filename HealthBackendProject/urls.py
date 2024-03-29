"""HealthBackendProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# commented code below used to generate swagger api
# to generate swagger api doc:
# a. uncomment the code below b. uncomment first path below c. uncomment drf_yasg from Installed app in settings.py
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
#
schema_view = get_schema_view(
   openapi.Info(
      title="eHealth API",
      default_version='v1',
      description="API's for mobile app ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ganymedecube@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('apidoc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), #view swagger api
    path('doctor/', include('Doctor.urls')),
    path('hospital/', include('Hospital.urls')),
    path('patient/', include('patient.urls')),
    path('jet/', include('jet.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls','jet-dashboard')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
