import json
import _thread
from kafka import KafkaConsumer, KafkaProducer

class KafkaObject(object):
    
    def __init__(self):
        self.kafkaConfig = self.kafka_config()

    def kafka_config(self):
        f = open('/home/ubuntu/kafka-helpers/kafkaip', 'r')
        config = f.readline()
        f.close()
        return config

class KafkaReader(KafkaObject):

    def __init__(self, topics=None, **kwargs):
        super(KafkaReader, self).__init__()
        self.DEFAULT_CONFIG = {}
        for key in kwargs:
            self.DEFAULT_CONFIG[key] = kwargs[key]
        self.topics = topics

    def consume(self, func):
        consumer = KafkaConsumer(bootstrap_servers=self.kafkaConfig, **self.DEFAULT_CONFIG)
        consumer.subscribe(topics=tuple(self.topics))

        for msg in consumer:
            func(msg.value.decode('utf-8'))

class KafkaWriter(KafkaObject):

    def __init__(self, json_msg=False, topic=None, threaded=False, **kwargs):
        super(KafkaWriter, self).__init__()
        self.DEFAULT_CONFIG = {}
        self.json = json_msg
        self.topic = topic
        self.threaded = threaded
        for key in kwargs:
            self.DEFAULT_CONFIG[key] = kwargs[key]
        self.DEFAULT_CONFIG['bootstrap_servers'] = self.kafkaConfig
        if json:
            self.DEFAULT_CONFIG['value_serializer'] = lambda v: json.dumps(v).encode('utf-8')

    def write(self, msg, topic=None):
        if self.threaded:
            _thread.start_new_thread(self.produce, (msg, topic,))
        else:
            self.produce(msg, topic)

    def produce(self, msg, topic=None):
        if topic is not None:
            self.topic = topic
        producer = KafkaProducer(**self.DEFAULT_CONFIG)
        producer.send(topic, msg).get(timeout=30)