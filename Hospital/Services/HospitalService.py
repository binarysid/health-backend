from Hospital.Services import logger
from Hospital.models.HospitalData import HospitalData
import base64, secrets, io
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
from HealthBackendProject.StatusCode import StatusCode
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, IntegrityError
from django.core.files.storage import FileSystemStorage

def get_image_from_data_url( data_url, resize=True, base_width=400 ):
    try:
        # getting the file format and the necessary dataURl for the file
        _format, _dataurl = data_url.split(';base64,')
        # file name and extension
        _filename, _extension   = secrets.token_hex(20), 'PNG'

        # generating the contents of the file
        file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

        # resizing the image, reducing quality and size
            # opening the file with the pillow
        image = Image.open(file)
            # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        if resize:
            w_percent = (base_width/float(image.size[0]))
            h_size = int((float(image.size[1])*float(w_percent)))
            image = image.resize((base_width,h_size), Image.ANTIALIAS)

            # save resized image
        image.save(image_io, format=_extension)

            # generating the content of the new image
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" )

        # file and filename
        return file, ( _filename, _extension )
    except:
        return None


def editHospitalInfo(id,logo):
    json_data = {}
    try:
        data = HospitalData.objects.get(id=id)
        if logo is not None:
            imageFile = get_image_from_data_url(logo, data)
            data.logo = imageFile[0]
        data.save()
        json_data = {'code': StatusCode.HTTP_200_OK.value, 'message': 'info updated'}
    except IntegrityError as e:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': e.args[1]}
    except:
        json_data = {'code': StatusCode.HTTP_400_BAD_REQUEST.value, 'message': 'no account found'}
    return json_data