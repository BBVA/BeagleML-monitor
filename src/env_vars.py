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
import os
import sys
import logging


def print_env_vars(config):
    print("Configuration parameters: ")
    for key in config:
        print(key + ": " + repr(config[key]))


def log_env_vars(config):
    logging.info("Configuration parameters: ")
    for key in config:
        logging.info("%s: %s", key, config[key])


def read_env_variables():
    config = {}
    try:
        config["KAFKA_SERVERS"] = os.getenv("KAFKA_SERVERS")
        config["KAFKA_GROUP"] = os.getenv("KAFKA_GROUP")
        config["LOG_CONFIG_FILE"] = os.getenv("LOG_CONFIG_FILE")
        config["MAIN_TOPIC"] = os.getenv("MAIN_TOPIC")
        config["MONGO_URL"] = os.getenv("MONGO_URL")
        # config["MONGO_PORT"]=int(os.getenv("MONGO_PORT"))
        config["MONGODB_DATABASE"] = os.getenv("MONGODB_DATABASE")
        config["MONGODB_USER"] = os.getenv("MONGODB_USER")
        config["MONGODB_PASSWORD"] = os.getenv("MONGODB_PASSWORD")
        return config
    except ValueError as e:
        sys.stderr.write("Error parsing environment variables\n")
        logging.error("Error parsing environment variables\n")
        sys.stderr.write(e)
        logging.error(e)
        sys.exit(-1)
