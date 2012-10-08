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
        'link' : {
            'rel' : opds.NEW,
            'href' : '/opds/new',
            'type' : opds.ACQUISITION}
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/publishers',
        'title' : 'Publishers', 
        'updated' : '2012-09-29T19:27:01Z',
        'link' : {
            'rel' : opds.SUBSECTION,
            'href' : '/opds/publishers',
            'type' : opds.NAVIGATION}
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/alpha', 
        'title' : 'Alphabetical', 
        'updated' : '2012-09-29T19:27:01Z',
        'link' : {
            'rel' : opds.SUBSECTION,
            'href' : '/opds/alpha',
            'type' : opds.NAVIGATION}
        })
    return {'entry': entry, 'link': link}
