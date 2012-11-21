from datetime import datetime
from models import Catalog, Alphabetical, Publisher, Book
from opds import LinkRel, ContentType, make_link
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pymongo import DESCENDING


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
    """ OPDS Catalog Alpha /opds/alpha
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/alpha')]

    alpha = Catalog.get('alpha')
    if not alpha:
        alpha = {'entry': [], 'updated': datetime.now()}

    return {
        '_id': 'http://books.scielo.org/opds/alpha',
        'title': 'SciELO Books - Alphabetical',
        'links': link,
        'entry': alpha['entry'],
        'updated': alpha['updated']}


@view_config(route_name='alpha_filter', renderer='opds')
def alpha_filter(request):
    """ OPDS Alpha filter for books
    """
    _id = request.matchdict['id']
    alpha = Alphabetical.get(_id)
    if not alpha:
        raise HTTPNotFound()

    link = [make_link('up', ContentType.NAVIGATION, '/opds/alpha'),
        make_link('self', ContentType.NAVIGATION,
            u'/opds/alpha/{}'.format(_id))]

    return {
        '_id': u'http://books.scielo.org/opds/alpha/{}'.format(_id),
        'title': u'SciELO Books - Filter starting with "{}"'.format(_id),
        'updated': alpha['updated'],
        'links': link,
        'entry': alpha['entry']}


@view_config(route_name='publisher_catalog', renderer='opds')
def publisher_catalog(request):
    """ OPDS Catalog Publishers /opds/publisher
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/publisher')]

    pub = Catalog.get('publisher')
    if not pub:
        pub = {'entry': [], 'updated': datetime.now()}

    return {
        '_id': 'http://books.scielo.org/opds/publisher',
        'title': 'SciELO Books - Publishers',
        'updated': pub['updated'],
        'links': link,
        'entry': pub['entry']}


@view_config(route_name='publisher_filter', renderer='opds')
def publisher_filter(request):
    """ OPDS Catalog Publisher filter for books
    """
    _id = request.matchdict['id']
    pub = Publisher.get(_id)
    if not pub:
        raise HTTPNotFound

    link = [make_link('up', ContentType.NAVIGATION, '/opds/publisher'),
        make_link('self', ContentType.NAVIGATION,
            '/opds/publisher/{}'.format(_id))]

    return {
        '_id': 'http://books.scielo.org/opds/publisher/{}'.format(_id),
        'title': 'SciELO Books - Filter for publisher "{}"'.format(_id),
        'updated': pub['updated'],
        'links': link,
        'entry': pub['entry']}


@view_config(route_name='new', renderer='opds')
def new(request):
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/new')]

    book = [b for b in Book.find().sort('updated', DESCENDING).limit(50)]

    return {
        '_id': 'http://books.scielo.org/opds/new',
        'title': 'SciELO Books - New Releases',
        'updated': datetime.now(),
        'links': link,
        'entry': book}