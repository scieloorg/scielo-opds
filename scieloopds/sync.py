import logging
import urllib2
import json
from datetime import datetime
from urllib import urlencode, quote
from opds import LinkRel, ContentType, make_link
from pymongo import Connection

import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__package__)

_db_host = 'localhost'
_db_port = 27017
_db_name = __package__
_rest_alpha = 'http://books.scielo.org/api/v1/alphasum/'
_rest_publisher = 'http://books.scielo.org/api/v1/publishers/'
_rest_book = 'http://books.scielo.org/api/v1/books/'

conn = Connection(_db_host, _db_port)
db = conn[_db_name]


def rest_fetch(url, **kwargs):
    params = urlencode([(k, v.encode('utf-8')) for k, v in kwargs.items()])
    req = urllib2.Request(url, params)
    log.info('fetching <%s%s>' % (url, '?' + params if params else ''))
    resp = urllib2.urlopen(req)
    data = json.load(resp)
    return data


def get_catalog(_id, url, link_builder=None, **kwargs):
    try:
        data = rest_fetch(url, **kwargs)
        catalog = {}
        catalog['_id'] = _id
        catalog['updated'] = datetime.now()
        entries = []
        for entry in data:
            updated = entry.get('updated', None)
            if updated:
                entry['updated'] = datetime.strptime(updated,
                    '%Y-%m-%d %H:%M:%S.%f')
            else:
                entry['updated'] = catalog['updated']
            if link_builder:
                entry['links'] = link_builder(entry)
            if 'total_items' in entry:
                entry['content'] = {'value':
                    u'{:d} item(s)'.format(entry['total_items'])}
            entries.append(entry)
        catalog['entry'] = entries
        return catalog
    except urllib2.URLError as e:
        log.error('%s:%s <%s>' % (e.__class__.__name__, e.message, e.url))


def link_factory(base_url):
    def f(entry):
        link = make_link(LinkRel.SUBSECTION, ContentType.ACQUISITION,
            base_url.format(quote(entry['_id'].encode('utf-8'))))
        return (link, )
    return f


def main(**settings):
    log.info('starting synchronization')
    alpha_index = get_catalog('alpha', _rest_alpha,
        link_builder=link_factory('/opds/alpha/{}'))
    if alpha_index:
        db.catalog.remove()
        db.catalog.save(alpha_index)
        for entry in alpha_index['entry']:
            alpha = get_catalog(entry['_id'], _rest_book,
                filter_initial=entry['_id'])
            if alpha:
                db.alpha.save(alpha)
            else:
                log.warning('Resource {0} returns empty catalog.'.
                    format('?'.join(_rest_book,
                        'filter_initial=' + entry['_id'])))
    else:
        log.warning('Resource {0} returns empty catalog.'.format(_rest_alpha))

    pub_index = get_catalog('publisher', _rest_publisher,
        link_builder=link_factory('/opds/publisher/{}'))
    if pub_index:
        db.catalog.save(pub_index)
        for entry in pub_index['entry']:
            pub = get_catalog(entry['_id'], _rest_book,
                filter_pulisher=entry['_id'])
            if pub:
                db.publisher.save(pub)
            else:
                log.warning('Resource {0} returns emptry catalog.'.
                    format('?'.join(_rest_book,
                        'filter_publisher=' + entry['_id'])))
    else:
        log.warning('Resource {0} returns empty catalog.'.
            format(_rest_publisher))

    #new = get_catalog('new', _rest_book)
    new = rest_fetch(_rest_book)
    if new:
        for book in new:
            updated = book.get('updated', None)
            if updated:
                book['updated'] = datetime.strptime(updated,
                    '%Y-%m-%d %H:%M:%S.%f')
            else:
                book['updated'] = datetime.now()
            db.book.save(book)
    else:
        log.warning('Resource {0} returns empty catalog.'.format(_rest_book))
    log.info('synchronization finish')

if __name__ == '__main__':
    main()