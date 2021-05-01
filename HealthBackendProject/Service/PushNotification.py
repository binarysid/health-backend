from HealthBackendProject.Service import Firebase

def initialize():
    Firebase.initApp()

def send_appntment_cancel_notification(appointment_info):
    messages = []
    for item in appointment_info:
        data = {
                'id': f'{item.id}',
                'message': f'your appointment of {item.visit_date} with doctor {item.doctor.name} has been cancelled',
            }
        message = Firebase.get_payload(data=data,
                                       reg_token=item.patient.notification_reg_token)
        messages.append(message)
        Firebase.send_batch_message(messages=messages)
