import os
import site
import errno
import shutil
from charmhelpers.core import hookenv, templating, unitdata
from charmhelpers.core.hookenv import status_set, charm_dir
from charmhelpers.contrib.python.packages import pip_install
from charms.reactive import when, when_not, set_state, remove_state

db = unitdata.kv()
kafka_config_path = '/home/ubuntu/kafka-helpers'


@when_not('kafkahelper.installed')
def install_kafkahelper():
    hookenv.log('Installing kafka-helper')
    pip_install('kafka-python')
    if not os.path.exists(kafka_config_path):
        os.makedirs(kafka_config_path)
    dis_packages = site.getsitepackages()[0]
    copy(charm_dir() + '/lib/charms/layer/kafkahelpers',
         dis_packages + '/kafkahelpers')
    status_set('blocked', 'Waiting for Kafka relation')
    set_state('kafkahelper.installed')


@when('kafka.joined')
@when_not('kafka.configured')
def configure_kafka(kafka):
    if kafka.kafkas():
        hookenv.log("Kafka relation found")
        open(kafka_config_path + '/kafkaip', 'w+').close()
        configure_kafka_info(kafka)
        set_state('kafka.configured')


@when('kafka.configured', 'kafka.ready')
@when_not('kafka.changed')
def update_kafkas(kafka):
    hookenv.log('Updating kafkas')
    if (db.get('kafka') != kafka.kafkas() or
            db.get('zookeeper') != kafka.zookeepers()):
        hookenv.log('New kafka configuration detected')
        configure_kafka_info(kafka)
        set_state('kafka.changed')


def configure_kafka_info(kafka):
    templating.render(
        source='kafka.connect',
        target=kafka_config_path + '/kafkaip',
        context={
            'units': kafka.kafkas(),
        }
    )
    db.set('kafka', kafka.kafkas())
    templating.render(
        source='kafka.connect',
        target=kafka_config_path + '/zookeeper',
        context={
            'units': kafka.zookeepers(),
        }
    )
    db.set('zookeeper', kafka.zookeepers())


@when('kafka.configured')
@when_not('kafka.joined')
def remove_kafka():
    hookenv.log("Kafka relation removed")
    if os.path.exists(kafka_config_path + '/kafkaip'):
        os.remove(kafka_config_path + '/kafkaip')
    status_set('blocked', 'Waiting for Kafka relation')
    remove_state('kafka.configured')


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            hookenv.log('Directory not copied')
