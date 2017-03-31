import os


def brokers_as_string(delimiter):
    brokers = []
    if os.path.exists('/home/ubuntu/kafka-helpers/kafkaip'):
        with open('/home/ubuntu/kafka-helpers/kafkaip') as f:
            content = f.readlines()
        brokers = [x.strip() for x in content]
    return delimiter.join(brokers)
