import os


def brokers_as_string(delimiter):
    brokers = []
    if os.path.exists('/home/ubuntu/kafka-helpers/kafkaip'):
        with open('/home/ubuntu/kafka-helpers/kafkaip') as f:
            content = f.readline().strip()
        brokers = content.split(',')
    return delimiter.join(brokers)
