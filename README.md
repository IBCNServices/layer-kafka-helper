# layer-kafka-helper
This charm provides some basic Kafka functionality such as storing ip/port from a related Kafka charm and a wrapper around the [kafka-python](http://kafka-python.readthedocs.io/en/master/) library.

# Usage
Include the layer in `layer.yaml`:
```yaml
includes: ['layer:kafka-helper']
```
## IP and port
When a relation is made with Kafka, ip and port configuration will be stored in `/home/ubuntu/kafka-helpers/kafkaip`. On completion, the state `kafka.configured` will be set.
This info will also be stored in the unitdata.kv with 'kafka' as key:

```
from charmhelpers.core import unitdata

db = unitdata.kv()
db.get('kafka')
```

## kafkahelper wrapper
The layer provides two wrapper classes, KafkaReader and KafkaWriter, representing a KafkaConsumer and KafkaProducer respectively. The layer will install the module in the python path, using the module can be done using:
```
from kafkahelpers.kafkahelper import KafkaReader, KafkaWriter
```


### KafkaReader
The reader needs at least one argument, namely a list with topics. 
```
t = ['topic1', 'topic2']
reader = KafkaReader(topics=t)
```
Additional [configuration parameters](http://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html) can be used to initialize the KafkaReader. As an example if we want to read from the start of a topic with a specified consumer group:
```
reader = KafkaReader(topics='topic1', auto_offset_reset='earliest', group_id='group1')
```
To start the consumer we need a function to perform actions with the incoming messages. For this the consume(func) method can be used. If we simply want to print all incoming messages to screen we could use:
```
def print_to_screen(msg):
    print(msg)
reader = KafkaReader(topics='topic1')
reader.consume(func=print_to_screen)
```
If more arguments are needed for the method, lambda functions can be used:
```
def print_to_screen(msg, extra):
    print(msg + extra)
reader = KafkaReader(topics='topic1')
reader.consume(func=lambda x: print_to_screen(x, 'extra parameter'))
```

### KafkaWriter
The writer has the same configuration parameters as described [here](http://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html) and some extra configuration options. 
Initializing the writer gives you the option to specify wheter you want to send json messages. A topic can be set when the reader is created or when the write() method is called. Finally the threaded option specifies wheter the messages are send via thread. The init signature is the following:
```
def __init__(self, json=False, topic=None, threaded=False, **kwargs):
```
As a full example, we read from a topic, print the content of the message, add another field and store it in another topic:
```
import json
from kafkahelpers.kafkahelper import KafkaReader, KafkaWriter

def print_and_store(msg, writer)
    print(msg)
    msg_dictionary = json.loads(msg)
    msg_dictionary['extra_field'] = 'ok'
    writer.write(msg_dictionary)
    
writer = KafkaWriter(json=True, topic='topic1.log')
reader = KafkaReader(group_id='topic1-group')
reader.consume(func=lambda x: print_and_store(x, writer))
```

## Authors

This software was created in the [IBCN research group](https://www.ibcn.intec.ugent.be/) of [Ghent University](http://www.ugent.be/en) in Belgium. This software is used in [Tengu](http://tengu.intec.ugent.be), a project that aims to make experimenting with data frameworks and tools as easy as possible.

 - Sander Borny <sander.borny@intec.ugent.be>
