from faker import Faker
import random
import json
from kafka import KafkaProducer
import time, datetime
KAFKA_SERVER = "3.87.240.251"
KAFKA_PORT = "9092"


class Generate():
    def __init__(self, topic):
        self.server = f'{KAFKA_SERVER}:{KAFKA_PORT}'
        self.topic = topic

    def __generate_events(self):
        fake = Faker()
        event = {
            "event_type": random.choice(["view", "purchase", "cart_update"]),
            "user_id": fake.uuid4(),
            "product_id": random.randint(1, 5),
            "price": round(random.uniform(10, 500), 2),
            "timestamp": datetime.datetime.now().isoformat()
        }
        return event
    
    
    def start_producer(self):
        producer = KafkaProducer(bootstrap_servers = self.server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        while True:
            event = self.__generate_events()
            producer.send(self. topic, value = event)
            time.sleep(10)

if __name__ == "__main__":
    produce_data = Generate('user_activity')
    produce_data.start_producer()