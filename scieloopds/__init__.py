# coding: utf-8
"""
.. module: scieloopds
   :synopsis: WSGI Application to provide SciELO Books in OPDS protocol.

.. moduleauthor:: Allison Vollmann <allisonvoll@gmail.com>

Example configuration (aditional parameters):
.. note::
   [app:main]
   ...
   mongo_uri = mongodb://localhost:27017/scieloopds
   scielo_uri = http://books.scielo.org/api/v1/
   auto_sync = True
   auto_sync_interval = 60
   items_per_page = 20
"""
import os
import sys
import logging
from urlparse import urlparse
from datetime import datetime, timedelta

import pymongo
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.settings import asbool

from .sync import main as do_sync
from .utils import get_db_connection


APP_PATH = os.path.abspath(os.path.dirname(__file__))


DEFAULT_SETTINGS = [
        ('mongo_uri', 'OPDS_MONGO_URI', str,
            'mongodb://localhost:27017/scieloopds'),
        ('scielo_uri', 'OPDS_SCIELO_URI', str,
            'http://books.scielo.org/api/v1'),
        ('auto_sync', 'OPDS_AUTO_SYNC', bool,
            True),
        ('auto_sync_interval', 'OPDS_AUTO_SYNC_INTERVAL', int,
            60*60*12),
        ('items_per_page', 'OPDS_ITEMS_PER_PAGE', int,
            20),
        ]


def parse_settings(settings):
    """Analisa e retorna as configurações da app com base no arquivo .ini e env.

    As variáveis de ambiente possuem precedência em relação aos valores
    definidos no arquivo .ini.
    """
    parsed = {}
    cfg = list(DEFAULT_SETTINGS)

    for name, envkey, convert, default in cfg:
        value = os.environ.get(envkey, settings.get(name, default))
        if convert is not None:
            value = convert(value)
        parsed[name] = value

    return parsed


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=parse_settings(settings))
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/opds/')
    config.add_route('new', '/opds/new')
    config.add_route('alpha_catalog', '/opds/alpha')
    config.add_route('alpha_filter', '/opds/alpha/{id}')
    config.add_route('publisher_catalog', '/opds/publisher')
    config.add_route('publisher_filter', '/opds/publisher/{id}')

    config.add_subscriber(add_mongo_db, NewRequest)
    config.add_subscriber(start_sync, NewRequest)
    config.scan(ignore='scieloopds.tests')
    config.add_renderer('opds', factory='scieloopds.renderers.opds_factory')
    return config.make_wsgi_app()


def ensure_indexes(db):
    db.book.ensure_index([('updated', pymongo.DESCENDING)])
    db.book.ensure_index([('title_ascii', pymongo.ASCENDING)])
    db.alpha.ensure_index([('title_ascii', pymongo.ASCENDING)])
    db.publisher.ensure_index([('title_ascii', pymongo.ASCENDING)])


def add_mongo_db(event):
    settings = event.request.registry.settings
    db = get_db_connection(settings)
    ensure_indexes(db)
    event.request.db = db


def start_sync(event):
    settings = event.request.registry.settings
    if settings['auto_sync']:
        db = event.request.db
        interval = settings['auto_sync_interval']
        try:
            update = db.catalog.find_one()
            if update:
                last_update = update['updated']
                next_update = last_update + timedelta(seconds=interval)
                if next_update < datetime.now():
                    do_sync(settings)
            else:
                do_sync(settings)
        except pymongo.errors.AutoReconnect as e:
            logging.getLogger(__name__).error('MongoDB: %s' % e.message)

