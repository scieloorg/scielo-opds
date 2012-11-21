from pymongo import Connection


class Mongo(object):

    _db_host = 'localhost'
    _db_port = 27017
    _db_name = __package__
    _db = None

    @classmethod
    def get_connection(cls):
        if not cls._db:
            cls._db = Connection(cls._db_host, cls._db_port)[cls._db_name]
        return cls._db

    @classmethod
    def get_collection(cls, collection):
        return cls.get_connection()[collection]

    def __init__(self, resource):
        self.resource = resource

    def get(self, _id):
        col = self.get_collection(self.resource)
        data = col.find_one({'_id': _id})
        return data

    def find(self, **kwargs):
        col = self.get_collection(self.resource)
        return col.find(**kwargs)


class Model(object):

    @classmethod
    def get(cls, _id):
        return cls.manager.get(_id)

    @classmethod
    def find(cls, **kwargs):
        return cls.manager.find(**kwargs)


class Catalog(Model):
    manager = Mongo('catalog')


class Publisher(Model):
    manager = Mongo('publisher')


class Alphabetical(Model):
    manager = Mongo('alpha')


class Book(Model):
    manager = Mongo('book')