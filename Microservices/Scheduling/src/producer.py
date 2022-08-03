import json
from sseclient import SSEClient as EventSource
from kafka import KafkaProducer

# Create producer
producer = KafkaProducer(
    bootstrap_servers='10.152.48.69:29092', #Kafka server
    value_serializer=lambda v: json.dumps(v).encode('utf-8') #json serializer
)

def sendNotification(notification):
    producer.send('notificationEvent', json.loads(notification))