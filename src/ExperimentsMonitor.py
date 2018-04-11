"""
Copyright 2018 Banco Bilbao Vizcaya Argentaria, S.A.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from confluent_kafka import Consumer, KafkaError
from ExperimentListener import ExperimentListener
import threading
import time
import logging
import DbConnector


class ExperimentsMonitor:
    def __init__(self, kafka_topic, kafka_servers, kafka_group_id, logger, db):
        self.topic_scheduler_communication = kafka_topic
        self.servers = kafka_servers
        self.group_id = None if kafka_group_id == "" else kafka_group_id
        self.consumer = Consumer({'bootstrap.servers': self.servers, 'group.id': self.group_id,
                                  'default.topic.config': {'auto.offset.reset': 'smallest'}})
        self.log = logger
        self.threads = []
        self.db = db

    def listen(self):
        """
        Subscribe to scheduler-monitor topic to receive messages from the scheduler.
        Each message brings a 'topic name' where a certain experiment is going to produce its metrics.
        Then, for each 'topic-name' received, an 'Experiment Listener' is created.
        """
        self.consumer.subscribe([self.topic_scheduler_communication])
        self.log.info("Monitor running! Subscribed to topic: %s \n Listening... " % self.topic_scheduler_communication)
        monitor_running = True

        while monitor_running:
            msg = self.consumer.poll(timeout=0.1)
            if msg != None:
                if not msg.error():
                    metrics_topic_to_listen = msg.value().decode('utf-8')
                    listener = ExperimentListener(metrics_topic_to_listen, self.servers, self.group_id, self.log,
                                                  self.db)
                    listener.start()
                    self.threads.append(listener)
                    self.log.info('Listener started! Listening topic: %s . Active threads: %d ',
                                  metrics_topic_to_listen, threading.active_count())
                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    self.log.error(msg.error())
                    monitor_running = False
            else:
                time.sleep(5)

        self.consumer.close()
