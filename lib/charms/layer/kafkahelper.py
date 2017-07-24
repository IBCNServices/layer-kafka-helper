from charmhelpers.core import unitdata


def brokers_as_string(delimiter):
    kafkas = unitdata.kv().get('kafka', [])
    brokers = []
    for kafka_unit in kafkas:
        brokers.append(kafka_unit['host'] + ':' + str(kafka_unit['port']))
    return delimiter.join(brokers)


def zookeepers_as_string(delimiter):
    zookeepers = unitdata.kv().get('zookeeper', [])
    brokers = []
    for zookeeper_unit in zookeepers:
        brokers.append(zookeeper_unit['host'] + ':' + str(zookeeper_unit['port']))
    return delimiter.join(brokers)
