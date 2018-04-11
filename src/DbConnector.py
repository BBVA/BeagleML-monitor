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
import time


class DbConnector:

    def __init__(self, logger):
        self.log = logger

    def connect_mongo(
            self, db_name='beagleml', password='P4fQMKF7yERFddXu',
            user='user0LT', url='172.30.23.2'):
        """Connect with the db and returns the db object."""
        self.log.info("database:")
        self.log.info('mongodb://' + user + ':' + password + '@' + url + '/' + db_name)
        client = MongoClient('mongodb://' + user + ':' + password + '@' + url + '/' + db_name)
        db = client[db_name]
        retries = 0
        while retries < 10:
            try:
                self.check_connection(db)
            except Exception as ex:
                self.log.warning('NO DATABASE CONNECTION')
                self.log.error(ex)
                retries += 1
                time.sleep(5)
            else:
                self.log.info('Database successfuly connected')
                break
        if retries is 10:
            self.log.critical('FAILED TO CONNECT THE DATABASE')
        return db

    def create_collection(self, collection_name, db):
        """Create the collection. Return True if succed or False if exists."""
        self.log.debug("Connecting to db")
        collection_names = db.collection_names()
        self.log.debug("collection names received")
        if collection_name not in collection_names:
            db.create_collection(collection_name)
            self.log.debug("Collection created")
            return True
        else:
            self.log.debug("Collection already exists")
            return True

    def check_connection(self, db):
        """Check the connection creating a collection."""
        self.log.debug("Checking db connection")
        return self.create_collection("__test_connection", db)
