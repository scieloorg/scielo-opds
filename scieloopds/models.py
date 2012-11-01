import json
import urllib
#import urllib2_mock as urllib2
import urllib2

class Rest(object):

    def __init__(self, resource):
        self.resource = resource

    def get(self, _id):
        return self.filter(_id = _id)

    def filter(self, **kwargs):
        params = urllib.urlencode(
            [(k, v.encode('utf-8')) for k,v in kwargs.items()])
        req = urllib2.Request(self.resource, params)
        resp = urllib2.urlopen(req)
        return resp

class Model(object):

    @classmethod    
    def get(cls, _id):
        return json.load(cls.manager.get(_id))

    @classmethod
    def filter(cls, **kwargs):
        return json.load(cls.manager.filter(**kwargs))

class Publisher(Model):
    manager = Rest('http://books.scielo.org/api/v1/publishers/')

class Alphabetical(Model):
    manager = Rest('http://books.scielo.org/api/v1/alphasum/')

class Book(Model):
    manager = Rest('http://books.scielo.org/api/v1/books/')
