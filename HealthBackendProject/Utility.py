from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import base64, secrets, io, os
from HealthBackendProject import LogHandler
logger = LogHandler.getLogHandler(filename='hospital.log')

def removeFile(path):
    try:
        os.remove(path=path)
    except:
        print('error')

def convertBase64ToImageFile(url, id):
    imgdata = base64.b64decode(url)
    filename = f'{id}.jpg'
    file = ContentFile(imgdata, name=filename)
    return file

def get_image_from_data_url( data_url, resize=True, base_width=1365 ):
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
