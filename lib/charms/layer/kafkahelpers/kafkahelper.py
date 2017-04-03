import json as json_module
import _thread
from kafka import KafkaConsumer, KafkaProducer

class KafkaObject(object):
    
    def __init__(self):
        self.kafkaConfig = self.kafka_config()

    def kafka_config(self):
        f = open('/home/ubuntu/kafka-helpers/kafkaip', 'r')
        config = f.readline().strip()
        f.close()
        return config.split(',')

class KafkaReader(KafkaObject):

    def __init__(self, topics=None, **kwargs):
        super(KafkaReader, self).__init__()
        self.DEFAULT_CONFIG = {}
        for key in kwargs:
            self.DEFAULT_CONFIG[key] = kwargs[key]
        self.topics = [topics] if isinstance(topics, str) else topics

    def consume(self, func):
        consumer = KafkaConsumer(bootstrap_servers=self.kafkaConfig, **self.DEFAULT_CONFIG)
        consumer.subscribe(topics=self.topics)

        for msg in consumer:
            func(msg.value.decode('utf-8'))

class KafkaWriter(KafkaObject):

    def __init__(self, json=False, topic=None, threaded=False, **kwargs):
        super(KafkaWriter, self).__init__()
        self.DEFAULT_CONFIG = {}
        self.json = json
        self.topic = topic
        self.threaded = threaded
        for key in kwargs:
            self.DEFAULT_CONFIG[key] = kwargs[key]
        if json:
            self.DEFAULT_CONFIG['value_serializer'] = lambda v: json_module.dumps(v).encode('utf-8')
        self.producer = KafkaProducer(bootstrap_servers=self.kafkaConfig, **self.DEFAULT_CONFIG)

    def write(self, msg, topic=None):
        if self.threaded:
            _thread.start_new_thread(self.produce, (msg, topic,))
        else:
            self.produce(msg, topic)

    def produce(self, msg, topic=None):
        if topic is not None:
            self.topic = topic
        if not self.json:
            msg = msg.encode('utf-8')
        self.producer.send(self.topic, msg).get(timeout=30)