import time
from opds import LinkRel, ContentType
from pyramid.view import view_config

@view_config(route_name='root', renderer='opds')
def root(request):
    """ OPDS Catalog root /opds/
    """
    link = []
    link.append({
        'rel': 'self',
        'href': '/opds/',
        'type': ContentType.NAVIGATION
        })
    entry = []
    entry.append({
        '_id': 'http://books.scielo.org/opds/new', 
        'title' : 'New Releases', 
        'updated' : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'links' : [{
            'rel' : LinkRel.NEW,
            'href' : '/opds/new',
            'type' : ContentType.ACQUISITION}]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/publishers',
        'title' : 'Publishers', 
        'updated' : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'links' : [{
            'rel' : LinkRel.SUBSECTION,
            'href' : '/opds/publishers',
            'type' : ContentType.NAVIGATION}]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/alpha', 
        'title' : 'Alphabetical', 
        'updated' : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'links' : [{
            'rel' : LinkRel.SUBSECTION,
            'href' : '/opds/alpha',
            'type' : ContentType.NAVIGATION}]
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
        'type': ContentType.NAVIGATION})
    link.append({
        'rel': 'self',
        'href': '/opds/alpha',
        'type': ContentType.NAVIGATION})

    entry = [{
        '_id': 'http://books.scielo.org/opds/alpha/a', 
        'title': 'A',
        'content': {'value': '10 titles'},
        'updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'links': [{
            'rel': LinkRel.SUBSECTION,
            'type': ContentType.ACQUISITION,
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
        'type': ContentType.NAVIGATION})
    link.append({
        'rel': 'self',
        'href': '/opds/publisher',
        'type': ContentType.NAVIGATION})

    entry = [{
        '_id': 'http://books.scielo.org/opds/publisher/EDUFBA', 
        'title': 'EDUFBA',
        'updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'content': {'value': '125 titles'},
        'links': [{
            'rel': LinkRel.SUBSECTION,
            'type': ContentType.ACQUISITION,
            'href': '/opds/publisher/EDUFBA'}]
        }]

    return {
        '_id': 'http://books.scielo.org/opds/publisher',
        'title': 'SciELO Books - Publishers',
        'links': link,
        'entry': entry}

@view_config(route_name='new', renderer='opds')
def new(request):
    link = []
    link.append({
        'rel': 'up',
        'href': '/opds/',
        'type': ContentType.NAVIGATION})
    link.append({
        'rel': 'self',
        'href': '/opds/new',
        'type': ContentType.NAVIGATION})

    entry = [{
        '_id': 'http://books.scielo.org/id/37t', 
        'title': u'Compreendendo a complexidade socioespacial',
        'year': u'2009',
        'language': u'pt',
        'isbn': u'9788523205607',
        'publisher': u'EDUFBA',
        'updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'synopsis': u'O livro constr\u00f3i um di\u00e1logo entre pesquisador',
        'cover': {
            'filename': 'http://books.scielo.org/id/37t/cover/cover.jpeg',
            'type': 'image/jpeg'},
        'cover_thumbnail': {
            'filename': ('http://books.scielo.org/id/37t/cover/'
                'cover_thumbail.jpeg'),
            'type': 'image/jpeg'},
        'pdf_file': {
            'filename': ('http://books.scielo.org/id/37t/pdf/'
                'ribeiro-9788523205607.pdf')},
        'creators': [[
            ['full_name', 'Ribeiro, Maria Teresa Franco']]],
        'links': [{
            'type': ContentType.ACQUISITION,
            'rel': LinkRel.ALTERNATE,
            'href': '/opds/book/37t'},
        {
            'type': ContentType.ACQUISITION,
            'rel': LinkRel.ACQUISITION,
            'href': ('http://books.scielo.org/id/37t/epub/'
                'ribeiro-9788523205607.epub')}]
        }]

    return {
        '_id': 'http://books.scielo.org/opds/new',
        'title': 'SciELO Books - New Releases',
        'links': link,
        'entry': entry}