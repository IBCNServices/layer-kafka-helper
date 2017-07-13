import os
from charmhelpers.core import unitdata

def brokers_as_string(delimiter):
    brokers = unitdata.kv().get('kafka', [])
    return delimiter.join(brokers)

def zookeepers_as_string(delimiter):
    zookeepers = unitdata.kv().get('zookeeper', [])
    return delimiter.join(zookeepers)
