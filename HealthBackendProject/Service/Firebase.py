import firebase_admin
from firebase_admin import credentials,db,messaging
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_json = os.path.join(BASE_DIR, 'ehealth-51077-firebase-adminsdk-m6y8b-8785518679.json')
cred = credentials.Certificate(cred_json)

def initApp():
    firebase_admin.initialize_app(cred,{
        'databaseURL':'https://ehealth-51077-default-rtdb.firebaseio.com/'
    })

def get_payload(data,reg_token):
    return messaging.Message(
        data=data, token=reg_token,
    )

def send_batch_message(messages):
    response = messaging.send_all(messages)
    print('{0} messages were sent successfully'.format(response.success_count))

def send_push_to_device(reg_token):
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=reg_token,
    )
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

def send_push_to_devices(reg_tokens):
    message = messaging.MulticastMessage(
        data={'score': '850', 'time': '2:45'},
        tokens=reg_tokens,
    )
    response = messaging.send_multicast(message)
    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(reg_tokens[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))

def send_message_to_topic():
    topic = 'highScores'

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

def subscribe_to_topic(reg_tokens,topic):
    response = messaging.subscribe_to_topic(reg_tokens, topic)
    print(response.success_count, 'tokens were subscribed successfully')

def unsubscribeToTopic(tokens,topic):
    response = messaging.unsubscribe_from_topic(tokens, topic)
    print(response.success_count, 'tokens were subscribed successfully')
