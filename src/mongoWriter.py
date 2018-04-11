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
from pymongo import MongoClient
from pymongo.database import Database
from bson.objectid import ObjectId
import logging


class mongoWriter:
    def __init__(self, db, logger, docName):
        self.log = logger
        self.db = db
        # self.check_connection()
        self.docName = docName
        self.metricsCollection = "experimentsMetrics"
        doc_query = {"name": self.docName}
        doc_update = {"name": self.docName, "metrics": []}

        r = self.db[self.metricsCollection].update_one(doc_query, {'$set': doc_update}, upsert=True)
        self.log.debug("Mongo update response: " + repr(r))
        if (r.upserted_id != None or r.matched_count > 0):
            self.log.debug("Metrics insert begins: " + self.docName)
        else:
            self.log.warning("Metrics insert failed: " + self.docName)

    def write_metrics(self, metrics):
        coll_name = self.metricsCollection
        doc_query = {"name": self.docName}

        r = self.db[coll_name].update_one(doc_query, {'$push': {'metrics': {'$each': [metrics], '$sort': {'time': 1}}}})
        self.log.debug("Mongo update response: " + repr(r))

        if (r.upserted_id != None or r.matched_count > 0):
            self.log.debug("Metrics updated: " + self.docName)
            return True
        else:
            self.log.warning("Metrics update failed: " + self.docName)
            return False
        return None

    def create_collection(self, coll_name):
        """Create the collection. Return True if succed or False if exists."""
        coll_names = self.db.collection_names()
        self.log.debug("collection names received")
        # TODO: Error checking !!!!!!!!!!!!!!!!!!!
        if coll_name not in coll_names:
            self.db.create_collection(coll_name)
            self.log.warning("Collection created: " + coll_name)
            self.log.debug("Collection created")
            return True
        else:
            self.log.debug("Collection already exists")
            return True

    def check_connection(self):
        return self.create_collection("__test_connection")

    def update_experiment_state(self, experiment_id, new_state):
        '''
        Change the state of the experiment in DDBB to 'new_state' 
        '''
        self.log.debug("Updating experiment %s state to %s ", experiment_id, new_state)

        collection_name = "experiments"
        self.create_collection(collection_name)

        doc_query = {'_id': ObjectId(experiment_id)}
        doc_update = {'state': new_state}

        result = self.db[collection_name].update_one(doc_query, {'$set': doc_update}, upsert=True)
        if (result.upserted_id != None or result.matched_count > 0):
            self.log.debug("State updated for experiment: " + experiment_id)
            if result.matched_count == 0:
                self.log.warning("Experiement does not exist. Created: " + experiment_id)
        else:
            self.log.warning("FAILED to update state for experiment: " + experiment_id)


if __name__ == "__main__":
    import yaml
    import logging.config

    with open("logging.yaml", 'r') as logconfig:
        cfg = yaml.safe_load(logconfig)

    logging.config.dictConfig(cfg)
    logger = logging.getLogger('mainLogger')

    url = "10.42.117.13"
    port = 27017
    dbName = "beaglemlDB"
    docName = "duymmyMetrics"

    client = MongoClient(url, port)
    db = Database(client, dbName)

    mw = mongoWriter(db, logger, docName)

    metric = {"time": 1}
    mw.write_metrics(metric)
