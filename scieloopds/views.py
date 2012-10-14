import opds
from pyramid.view import view_config

@view_config(route_name='root', renderer='opds')
def root(request):
    """ OPDS Catalog root /opds/
    """
    link = []
    link.append({
        'rel': 'self',
        'href': '/opds/',
        'type': opds.NAVIGATION
        })
    entry = []
    entry.append({
        '_id': 'http://books.scielo.org/opds/new', 
        'title' : 'New Releases', 
        'updated' : '2012-09-29T19:27:01Z',
        'links' : [{
            'rel' : opds.NEW,
            'href' : '/opds/new',
            'type' : opds.ACQUISITION}]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/publishers',
        'title' : 'Publishers', 
        'updated' : '2012-09-29T19:27:01Z',
        'links' : [{
            'rel' : opds.SUBSECTION,
            'href' : '/opds/publishers',
            'type' : opds.NAVIGATION}]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/alpha', 
        'title' : 'Alphabetical', 
        'updated' : '2012-09-29T19:27:01Z',
        'links' : [{
            'rel' : opds.SUBSECTION,
            'href' : '/opds/alpha',
            'type' : opds.NAVIGATION}]
        })
    return {'entry': entry, 'links': link}


@view_config(route_name='alpha_catalog', renderer='opds')
def alpha_catalog(request):
    """ OPDS Catalog Alpha /opds/alpha
    """
    link = []
    link.append({
        'rel': 'up',
        'href': '/opds/',
        'type': opds.NAVIGATION})
    link.append({
        'rel': 'self',
        'href': '/opds/alpha',
        'type': opds.NAVIGATION})

    entry = [{
        '_id': 'http://books.scielo.org/opds/alpha/a', 
        'title': 'A',
        'content': '10 titles',
        'links': [{
            'rel': opds.SUBSECTION,
            'type': opds.ACQUISITION,
            'href': '/opds/alpha/a'}]
        }]

    return {
        '_id': 'http://books.scielo.org/opds/alpha',
        'title': 'SciELO Books - Alphabetical',
        'links': link,
        'entry': entry}

@view_config(route_name='publisher_catalog', renderer='opds')
def publisher_catalog(request):
    """ OPDS Catalog Publishers /opds/publisher
    """
    link = []
    link.append({
        'rel': 'up',
        'href': '/opds/',
        'type': opds.NAVIGATION})
    link.append({
        'rel': 'self',
        'href': '/opds/publisher',
        'type': opds.NAVIGATION})

    entry = [{
        '_id': 'http://books.scielo.org/opds/publisher/EDUFBA', 
        'title': 'EDUFBA',
        'content': '125 titles',
        'links': [{
            'rel': opds.SUBSECTION,
            'type': opds.ACQUISITION,
            'href': '/opds/publisher/EDUFBA'}]
        }]

    return {
        '_id': 'http://books.scielo.org/opds/publisher',
        'title': 'SciELO Books - Publishers',
        'links': link,
        'entry': entry}