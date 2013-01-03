"""
.. module: scieloopds.views
   :synopsis: Views.

.. moduleauthor:: Allison Vollmann <allisonvoll@gmail.com>
"""

from datetime import datetime
from .opds import LinkRel, ContentType, make_link, make_pagination_links
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pymongo import ASCENDING, DESCENDING, errors
from urllib import quote, unquote
import logging


def paginate(cursor, page, items_per_page):
    return cursor.skip((page - 1) * items_per_page).limit(items_per_page)


@view_config(route_name='root', renderer='opds')
def root(request):
    """ OPDS Catalog root /opds/
    """
    link = [make_link(LinkRel.SELF, ContentType.NAVIGATION, '/opds/')]
    entry = []
    entry.append({
        '_id': 'http://books.scielo.org/opds/new',
        'title': 'New Releases',
        'updated': datetime.now(),
        'links': [make_link(LinkRel.NEW, ContentType.ACQUISITION,
            '/opds/new')]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/publisher',
        'title': 'Publishers',
        'updated': datetime.now(),
        'links': [make_link(LinkRel.SUBSECTION, ContentType.NAVIGATION,
            '/opds/publisher')]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/alpha',
        'title': 'Alphabetical',
        'updated': datetime.now(),
        'links': [make_link(LinkRel.SUBSECTION, ContentType.NAVIGATION,
            '/opds/alpha')]
        })
    return {'entry': entry, 'links': link}


@view_config(route_name='alpha_catalog', renderer='opds')
def alpha_catalog(request):
    """ OPDS Catalog alpha index /opds/alpha
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/alpha')]

    entry = []
    try:
        for alpha in request.db.alpha.find().sort('title_ascii', ASCENDING):
            if 'links' not in alpha:
                alpha['links'] = [make_link(LinkRel.SUBSECTION,
                    ContentType.ACQUISITION, '/opds/alpha/{}'.format(quote
                        (alpha['_id'].encode('utf8')))), ]
            entry.append(alpha)
    except errors.AutoReconnect as e:
        logging.getLogger(__name__).error('MongoDB: %s' % e.message)

    return {
        '_id': 'http://books.scielo.org/opds/alpha',
        'title': 'SciELO Books - Alphabetical',
        'links': link,
        'entry': entry,
        'updated': datetime.now()}


@view_config(route_name='alpha_filter', renderer='opds')
def alpha_filter(request):
    """ OPDS Alpha filter for books /opds/alpha/[LETTER]
    """
    _id = request.matchdict['id']
    result = request.db.book.find({'title': {'$regex': '^%s' % _id}}
        ).sort('title_ascii', ASCENDING)
    if not result:
        raise HTTPNotFound()

    base_url = '/opds/alpha/{}'.format(quote(_id.encode('utf-8')))
    link = [make_link('up', ContentType.NAVIGATION, '/opds/alpha'),
        make_link('self', ContentType.NAVIGATION, base_url)]

    entry = []
    try:
        try:
            items_per_page = int(
                request.registry.settings.get('items_per_page', 20))
        except ValueError:
            items_per_page = 20
        try:
            page = int(request.params.get('page', 1))
        except ValueError:
            page = 1

        link.extend(make_pagination_links(base_url, page, items_per_page,
            result.count()))

        for alpha in paginate(result, page, items_per_page):
            entry.append(alpha)
    except errors.AutoReconnect as e:
        logging.getLogger(__name__).error('MongoDB: %s' % e.message)

    return {
        '_id': 'http://books.scielo.org/opds/alpha/{}'.format(_id),
        'title': 'SciELO Books - Filter starting with "{}"'.format(_id),
        'updated': datetime.now(),
        'links': link,
        'entry': entry}


@view_config(route_name='publisher_catalog', renderer='opds')
def publisher_catalog(request):
    """ OPDS Catalog publishers index /opds/publisher
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/publisher')]

    entry = []
    try:
        for pub in request.db.publisher.find().sort('title_ascii', ASCENDING):
            if 'links' not in pub:
                pub['links'] = [make_link(LinkRel.SUBSECTION,
                    ContentType.ACQUISITION, '/opds/publisher/{}'.format(quote
                        (pub['_id'].encode('utf8')))), ]
            entry.append(pub)
    except errors.AutoReconnect as e:
        logging.getLogger(__name__).error('MongoDB: %s' % e.message)

    return {
        '_id': 'http://books.scielo.org/opds/publisher',
        'title': 'SciELO Books - Publishers',
        'updated': datetime.now(),
        'links': link,
        'entry': entry}


@view_config(route_name='publisher_filter', renderer='opds')
def publisher_filter(request):
    """ OPDS Catalog publisher filter for books /opds/publisher/[PUBLISHER]
    """
    _id = request.matchdict['id']
    result = request.db.book.find({'publisher': unquote(_id)}
        ).sort('title_ascii', ASCENDING)
    if not result:
        raise HTTPNotFound

    base_url = '/opds/publisher/{}'.format(quote(_id.encode('utf-8')))

    link = [make_link('up', ContentType.NAVIGATION, '/opds/publisher'),
        make_link('self', ContentType.NAVIGATION, base_url)]

    entry = []
    try:
        try:
            items_per_page = int(
                request.registry.settings.get('items_per_page', 20))
        except ValueError:
            items_per_page = 20
        try:
            page = int(request.params.get('page', 1))
        except ValueError:
            page = 1

        link.extend(make_pagination_links(base_url, page, items_per_page,
            result.count()))

        for pub in paginate(result, page, items_per_page):
            entry.append(pub)
    except errors.AutoReconnect as e:
        logging.getLogger(__name__).error('MongoDB: %s' % e.message)

    return {
        '_id': 'http://books.scielo.org/opds/publisher/{}'.format(_id),
        'title': 'SciELO Books - Filter for publisher "{}"'.format(
            unquote(_id)),
        'updated': datetime.now(),
        'links': link,
        'entry': entry}


@view_config(route_name='new', renderer='opds')
def new(request):
    """ OPDS Catalog new release /opds/new
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/new')]

    result = request.db.book.find().sort('updated', DESCENDING)

    if not result:
        raise HTTPNotFound

    entry = []
    try:
        try:
            items_per_page = int(
                request.registry.settings.get('items_per_page', 20))
        except ValueError:
            items_per_page = 20

        try:
            page = int(request.params.get('page', 1))
        except ValueError:
            page = 1

        link.extend(make_pagination_links('/opds/new', page, items_per_page,
            result.count()))

        for book in paginate(result, page, items_per_page):
            entry.append(book)
    except errors.AutoReconnect as e:
        logging.getLogger(__name__).error('MongoDB: %s' % e.message)

    return {
        '_id': 'http://books.scielo.org/opds/new',
        'title': 'SciELO Books - New Releases',
        'updated': datetime.now(),
        'links': link,
        'entry': entry}
