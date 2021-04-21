MEDIA_ROOT="health_project_media_files"
cd .. #this file will reside in project directory but we will create media dir outside(one level up the project directory) 
mkdir $MEDIA_ROOT

DOCTOR_DIR="$MEDIA_ROOT/doctor/"
HOSPITAL_DIR="$MEDIA_ROOT/hospital/"
PATIENT_DIR="$MEDIA_ROOT/patient/"
PROFILE_DIR="profile"

mkdir $DOCTOR_DIR
mkdir $HOSPITAL_DIR
mkdir $PATIENT_DIR
 
mkdir "$DOCTOR_DIR/$PROFILE_DIR/"
mkdir "$HOSPITAL_DIR/$PROFILE_DIR/"
mkdir "$PATIENT_DIR/$PROFILE_DIR/"
