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
from mongoWriter import mongoWriter
from MessageParser import MessageParser
import threading
import time

# TODO: Make a better special messages handling

expected_termination_messages = ("<TIMEOUT_REACHED>", "<ACCURACY_REACHED>", "<EXPERIMENT_COMPLETED>",
                                 '{"msg": "experiment_completed", "type": "service"}')  # ,"<EXPERIMENT_PAUSED>")


class ExperimentListener(threading.Thread):
    def __init__(self, kafka_topic, kafka_servers, kafka_group_id, logger, db):
        threading.Thread.__init__(self)
        self.consumer = Consumer({'bootstrap.servers': kafka_servers, 'group.id': kafka_group_id,
                                  'default.topic.config': {'auto.offset.reset': 'smallest'}})
        self.topic = kafka_topic
        self.experiment_id = kafka_topic.split('-')[0]  # Get experiment ID from topic name.
        self.log = logger
        self.parser = MessageParser(self.log)
        self.kafkaTimeout = 5
        self.db = db

    def run(self):
        self.log.info("[0x%x] Thread started, topic: %s", threading.get_ident(), self.topic)
        self.consumer.subscribe([self.topic])
        self.consume()

    def consume(self):
        running = True
        self.log.info("[0x%x] Listening to %s", threading.get_ident(), self.topic)
        writer = mongoWriter(self.db, self.log, self.topic)

        while running:
            msg = self.consumer.poll(timeout=self.kafkaTimeout)
            if msg != None:
                if not msg.error():
                    msgText = msg.value().decode('utf-8')
                    self.log.debug('[0x%x] Message received: %s', threading.get_ident(), msgText)
                    metrics = self.parser.parse_message(msgText)

                    if metrics != None:
                        self.log.debug('Metrics recieved - Writing metrics')
                        writer.write_metrics(metrics)

                    if msgText in expected_termination_messages:
                        self.log.info("[0x%x] Closing thread. Experiment %s ended because of: %s",
                                      threading.get_ident(), self.experiment_id, msgText)
                        if msgText == "<EXPERIMENT_COMPLETED>":
                            writer.update_experiment_state(self.experiment_id, "completed")
                        running = False

                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    self.log.error(msg.error())
                    running = False
            else:
                time.sleep(5)

        self.consumer.close()
