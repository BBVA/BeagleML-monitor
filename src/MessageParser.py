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
import re
import json


class MessageParser:
    def __init__(self, logger):
        self.log = logger

    def parse_message(self, message):
        if self.is_json(message):
            try:
                res = self.parse_json(message)
                return res
            except Exception as e:
                self.log.error("Error parsing message: " + message)
                self.log.error(e)
                return None
        else:
            return self.parse_basic(message)

    def is_json(self, message):
        return message[0] == '{' or message[0] == '['

    def parse_json(self, message):
        results = json.loads(message)
        if results["type"] == "metrics":
            return results["metrics"]
        else:
            self.log.info("Non metrics message: " + message)
            return None

    def parse_basic(self, results):
        prog = re.compile('[(\d|\self.)+\s]+')
        if not (prog.match(results[len(results) - 1]) and prog.match(results[0])):
            self.log.debug("Incorrect message format: " + results + " .Is it a termination message?")
            return None

        results = results.split("\t")

        if len(results) <= 1:
            self.log.debug("No elements found splitting the message: " + results + " It must use tabs")
            return None

        self.log.debug(results)
        results_list = {'cost': float(results[3]),
                        'accuracy': float(results[4]),
                        'time': float(results[0]),
                        'experimentTime': float(results[1]),
                        'batches': float(results[2])
                        }
        self.log.debug(results_list)
        return results_list


if __name__ == "__main__":
    import yaml
    import logging.config

    with open("logging.yaml", 'r') as logconfig:
        cfg = yaml.safe_load(logconfig)

    logging.config.dictConfig(cfg)
    logger = logging.getLogger('mainLogger')

    mp = MessageParser(logger)

    m1 = "1489487590.853008	73.23106098175049	22400	0.12118717	1.0"
    m2 = "Configuration parameters:"
    m3 = "LEARNING_RATE: 0.01"
    m4 = "OPTIMIZER: 'AdamOptimizer'"
    m6 = "{'metrics': {}}"
    m6 = '{"metrics": {"accuarcy": 0.68118918, "true_positives": 9094.0, "precision": 0.68396509, "experimentTime": 42.94835138320923, "false_negatives": 1696.0, "recall": 0.84281743, "epochs": 185000, "false_positives": 4202.0, "cost": 0.57189542, "time": 1513702617.1760187, "count": 185000}, "type": "metrics"}'
    m7 = "{'type': Error"
    print(mp.is_json(m6))
    print(mp.is_json(m3))
    print(mp.parse_message(m1))
    print(mp.parse_message(m6))
    print(mp.parse_message(m7))
