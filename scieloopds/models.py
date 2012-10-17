import json
import urllib
import mock_urllib as urllib2

class Rest(object):

    def __init__(self, resource):
        self.resource = resource

    def get(self, _id):
        return open(self.resource)

    def filter(self, **kwargs):
        return open(self.resource)

class Model(object):

    @classmethod    
    def get(cls, _id):
        return json.load(cls.manager.get(_id))

    @classmethod
    def filter(cls, **kwargs):
        return json.load(cls.manager.filter(**kwargs))

class Publisher(Model):
    manager = Rest('%s/fixtures/publishers_list.json' % __package__)

class Alphabetical(Model):
    manager = Rest('%s/fixtures/alpha_sum.json' % __package__)

class Book(Model):
    manager = Rest('%s/fixtures/37t.json' % __package__)
