from datetime import datetime
from opds import LinkRel, ContentType, make_link
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pymongo import ASCENDING, DESCENDING
from urllib import quote


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

    entry = []
    for alpha in request.db.alpha.find():
        if 'links' not in alpha:
            alpha['links'] = [make_link(LinkRel.SUBSECTION,
                ContentType.ACQUISITION, '/opds/alpha/{}'.format(quote
                    (alpha['_id'].encode('utf8')))), ]
        entry.append(alpha)

    return {
        '_id': 'http://books.scielo.org/opds/alpha',
        'title': 'SciELO Books - Alphabetical',
        'links': link,
        'entry': entry,
        'updated': datetime.now()}


@view_config(route_name='alpha_filter', renderer='opds')
def alpha_filter(request):
    """ OPDS Alpha filter for books
    """
    _id = request.matchdict['id']
    result = request.db.book.find({'title': {'$regex': '^%s' % _id}}
        ).sort('title', ASCENDING)
    if not result:
        raise HTTPNotFound()

    entry = []
    for alpha in result:
        entry.append(alpha)

    link = [make_link('up', ContentType.NAVIGATION, '/opds/alpha'),
        make_link('self', ContentType.NAVIGATION,
            u'/opds/alpha/{}'.format(_id))]

    return {
        '_id': u'http://books.scielo.org/opds/alpha/{}'.format(_id),
        'title': u'SciELO Books - Filter starting with "{}"'.format(_id),
        'updated': datetime.now(),
        'links': link,
        'entry': entry}


@view_config(route_name='publisher_catalog', renderer='opds')
def publisher_catalog(request):
    """ OPDS Catalog Publishers /opds/publisher
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/publisher')]

    entry = []
    for pub in request.db.publisher.find():
        if 'links' not in pub:
            pub['links'] = [make_link(LinkRel.SUBSECTION,
                ContentType.ACQUISITION, '/opds/publisher/{}'.format(quote
                    (pub['_id'].encode('utf8')))), ]
        entry.append(pub)

    return {
        '_id': 'http://books.scielo.org/opds/publisher',
        'title': 'SciELO Books - Publishers',
        'updated': datetime.now(),
        'links': link,
        'entry': entry}


@view_config(route_name='publisher_filter', renderer='opds')
def publisher_filter(request):
    """ OPDS Catalog Publisher filter for books
    """
    _id = request.matchdict['id']
    result = request.db.book.find({'publisher': _id}).sort('title', ASCENDING)
    if not result:
        raise HTTPNotFound

    entry = []
    for pub in result:
        entry.append(pub)

    link = [make_link('up', ContentType.NAVIGATION, '/opds/publisher'),
        make_link('self', ContentType.NAVIGATION,
            '/opds/publisher/{}'.format(_id))]

    return {
        '_id': 'http://books.scielo.org/opds/publisher/{}'.format(_id),
        'title': 'SciELO Books - Filter for publisher "{}"'.format(_id),
        'updated': datetime.now(),
        'links': link,
        'entry': entry}


@view_config(route_name='new', renderer='opds')
def new(request):
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/new')]

    result = request.db.book.find().sort('updated', DESCENDING).limit(50)
    if not result:
        raise HTTPNotFound

    entry = []
    for book in result:
        entry.append(book)

    return {
        '_id': 'http://books.scielo.org/opds/new',
        'title': 'SciELO Books - New Releases',
        'updated': datetime.now(),
        'links': link,
        'entry': entry}