import pymongo
from pyramid.config import Configurator
from pyramid.events import NewRequest
from urlparse import urlparse
from subprocess import Popen
from datetime import datetime, timedelta


def do_connect(db_conn, db_url):
    db = db_conn[db_url.path[1:]]
    if db_url.username and db_url.password:
        db.authenticate(db_url.username, db_url.password)
    return db


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/opds/')
    config.add_route('new', '/opds/new')
    config.add_route('alpha_catalog', '/opds/alpha')
    config.add_route('alpha_filter', '/opds/alpha/{id}')
    config.add_route('publisher_catalog', '/opds/publisher')
    config.add_route('publisher_filter', '/opds/publisher/{id}')

    # Create mongodb connection
    db_url = urlparse(settings['mongo_uri'])
    conn = pymongo.Connection(host=db_url.hostname, port=db_url.port)
    config.registry.settings['db_conn'] = conn

    # Create mongodb indexes
    db = do_connect(conn, db_url)
    db.book.ensure_index([('updated', pymongo.DESCENDING)])
    db.book.ensure_index([('title', pymongo.ASCENDING)])
    db.alpha.ensure_index([('title', pymongo.ASCENDING)])
    db.publisher.ensure_index([('title', pymongo.ASCENDING)])

    # Register mongodb connection in pyramid event subscriber
    def add_mongo_db(event):
        settings = event.request.registry.settings
        db = do_connect(settings['db_conn'], db_url)
        if settings.get('auto_sync', False):
            # 10 minutes default interval
            interval = settings.get('auto_sync_interval', 600)
            cmd = settings['auto_sync_cmd'].split()
            catalog = db.catalog.find_one()
            if catalog:
                last_updated = catalog['updated'] + timedelta(
                    seconds=int(interval))
                if last_updated < datetime.now():
                    Popen(cmd)
            else:
                Popen(cmd)

        event.request.db = db
    config.add_subscriber(add_mongo_db, NewRequest)

    config.scan()
    config.add_renderer('opds', factory='scieloopds.renderers.opds_factory')
    # Create indexes in mongodb
    return config.make_wsgi_app()
