from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import base64, secrets, io, os
from HealthBackendProject import LogHandler
from datetime import datetime, timedelta
from HealthBackendProject.Service import ExceptionLogger

logger = LogHandler.getLogHandler(filename='hospital.log')
timeFormat = '%H:%M'
timeFormatAmPm = '%H:%M %p'
dateFormate = '%Y-%m-%d'
date_format_YMD = '%Y-%m-%d'
date_format_DMY = '%d-%m-%Y'
time_format_24 = '%H:%M'
time_format_12 = '%I:%M'
time_format_24_am_pm = '%H:%M %p'
time_format_12_am_pm = '%I:%M %p'

def getTimeDiff(start_time,end_time,format):
    #fmt = '%I:%M %p' # %I gives 12 hours format & %H gives 24 hrs
    try:
        d1 = datetime.strptime(start_time, format)
        d2 = datetime.strptime(end_time, format)
        diff = d2 - d1
        diff_minutes = (diff.days * 24 * 60) + (diff.seconds / 60)
        return int(diff_minutes)
    except Exception as e:
        ExceptionLogger.track(e=e)

def getTimeRange(start_time,end_time,interval,format):
    start = datetime.strptime(start_time, format)
    end = datetime.strptime(end_time, format)
    def datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta
    try:
        return [dt.strftime(format) for dt in
           datetime_range(datetime(2016, 9, 1, start.hour,minute=start.minute), datetime(2016, 9, 1, end.hour, minute=end.minute),
                          timedelta(minutes=interval))]
    except Exception as e:
        ExceptionLogger.track(e=e)


def removeFile(path):
    try:
        os.remove(path=path)
    except Exception as e:
        ExceptionLogger.track(e=e)

def convertBase64ToImageFile(url, id):
    try:
        imgdata = base64.b64decode(url)
        filename = f'{id}.jpg'
        file = ContentFile(imgdata, name=filename)
        return file
    except Exception as e:
        ExceptionLogger.track(e=e)

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
    except Exception as e:
        ExceptionLogger.track(e=e)

def is_equal_to_week_day(date,day,format):
    try:
        p_date = datetime.strptime(date, format)
        week_day = p_date.strftime("%A")
        print(week_day)
        return day.lower()[:3]==week_day.lower()[:3]
    except Exception as e:
        ExceptionLogger.track(e=e)

def get_day_from(date,format):
    try:
        return date.strftime("%A").lower()
    except Exception as e:
        ExceptionLogger.track(e=e)