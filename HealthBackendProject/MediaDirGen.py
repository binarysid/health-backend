import os

MEDIA_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEDIA_ROOT = os.path.join(MEDIA_BASE_DIR, 'health_project_media_files/')

DOCTOR_ROOT = "doctor/"
HOSPITAL_ROOT = "hospital/"
PATIENT_ROOT = "patient/"

DOCTOR_DIR = f"{MEDIA_ROOT}/{DOCTOR_ROOT}"
HOSPITAL_DIR = f"{MEDIA_ROOT}/{HOSPITAL_ROOT}"
PATIENT_DIR = f"{MEDIA_ROOT}/{PATIENT_ROOT}"
PROFILE_DIR = "profile/"

DOCTOR_PROFILE_ROOT = f"{DOCTOR_ROOT}/{PROFILE_DIR}/"
HOSPITAL_PROFILE_ROOT = f"{HOSPITAL_ROOT}/{PROFILE_DIR}/"
PATIENT_PROFILE_ROOT = f"{PATIENT_ROOT}/{PROFILE_DIR}/"

DOCTOR_PROFILE_DIR = MEDIA_ROOT+'/'+DOCTOR_PROFILE_ROOT
HOSPITAL_PROFILE_DIR = MEDIA_ROOT+'/'+HOSPITAL_PROFILE_ROOT
PATIENT_PROFILE_DIR = MEDIA_ROOT+'/'+PATIENT_PROFILE_ROOT

# os.mkdir(MEDIA_ROOT)
# os.mkdir(DOCTOR_DIR)
# os.mkdir(HOSPITAL_DIR)
# os.mkdir(PATIENT_DIR)
#
# os.mkdir(DOCTOR_PROFILE_DIR)
# os.mkdir(PATIENT_PROFILE_DIR)
# os.mkdir(HOSPITAL_PROFILE_DIR)
#