import pymongo

from nlp.config import *

class MongoClient(object):
    def __init__(self):
        self._db = pymongo.MongoClient(MONGO_URL)[MONGO_DB]

    def get_meinv(self, **kwargs):
        for m in self._db[MONGO_TABLE].distinct(kwargs['key'], kwargs['filter']):
            yield m
    def put(self, **kwargs):
        self._db[kwargs['table']].insert(kwargs['data'])

    def get(self, **kwargs):
        for res in self._db[kwargs['table']].find(kwargs['query']):
            yield res['image_urls']