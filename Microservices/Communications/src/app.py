from kafka import KafkaConsumer
from json import loads
import json

consumer = KafkaConsumer(
    'notificationEvent',
     bootstrap_servers=['10.152.48.69:29092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8'))
)

def run():
    for message in consumer:
        message = message.value
        json_string = json.dumps(message) 
        notification = json.loads(json_string)
        sendEmail(notification['users'], notification['message'])

def sendEmail(users, message):
    #send email code