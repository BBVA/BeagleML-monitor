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
from ExperimentsMonitor import ExperimentsMonitor
import logging
import logging.config
import yaml
import env_vars as env
from DbConnector import DbConnector


def main():
    config = env.read_env_variables()

    with open(config["LOG_CONFIG_FILE"], 'r') as logconfig:
        cfg = yaml.safe_load(logconfig)

    logging.config.dictConfig(cfg)
    logger = logging.getLogger('mainLogger')

    env.log_env_vars(config)
    conn = DbConnector(logger)
    db = conn.connect_mongo(
        url=config["MONGO_URL"], db_name=config["MONGODB_DATABASE"],
        user=config["MONGODB_USER"], password=config["MONGODB_PASSWORD"])

    monitor = ExperimentsMonitor(
        config["MAIN_TOPIC"], config["KAFKA_SERVERS"],
        config["KAFKA_GROUP"], logger, db)
    monitor.listen()


if __name__ == "__main__":
    main()
