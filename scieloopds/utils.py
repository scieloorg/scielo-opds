# coding: utf-8
import sys
import logging

import pymongo

from urlparse import urlparse


def get_db_connection(settings):
    db_url = urlparse(settings['mongo_uri'])
    try:
        conn = pymongo.MongoClient(host=db_url.hostname, port=db_url.port)
    except pymongo.errors.ConnectionFailure as e:
        logging.getLogger(__name__).error('MongoDB: %s' % e.message)
        sys.exit(1)
    db = conn[db_url.path[1:]]
    return db
