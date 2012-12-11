import urllib2
import json
import logging
import pymongo
from scieloopds import do_connect
from threading import Thread
from datetime import datetime
from urlparse import urlparse, urljoin
from httplib import HTTPException
from unicodedata import normalize


def rest_fetch(url):
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    data = json.load(resp)
    return data


class SyncError(Exception):
    pass


class Sync(Thread):

    def __init__(self, src, dst, db):
        super(Sync, self).__init__()
        self.src = src
        self.dst = dst
        self.db = db

    def run(self):
        log = logging.getLogger('Sync')
        try:
            log.info('fetching <%s>' % self.src)
            now = datetime.now()
            data = rest_fetch(self.src)
            if not data:
                raise SyncError('Resource <%s> result is empty' %
                    self.src)

            for entry in data:
                updated = entry.get('updated', None)
                if updated:
                    entry['updated'] = datetime.strptime(updated,
                        '%Y-%m-%d %H:%M:%S.%f')
                else:
                    entry['updated'] = datetime.now()
                if 'total_items' in entry:
                    entry['content'] = {'type': 'text',
                        'value': '%s book(s)' % entry['total_items']}
                if 'publisher' in entry:
                    entry['publisher'] = entry['publisher'].upper()
                if 'title' in entry:
                    entry['title_ascii'] = normalize('NFKD', entry['title']
                        ).encode(errors='ignore').lower()
                self.db[self.dst].save(entry)

            self.db.catalog.update({'_id': 1}, {'$set': {self.dst: now}})

        except urllib2.URLError as e:
            log.error('%s:%s <%s> %s' % (e.__class__.__name__,
                e.message, e.url, e.msg))
        except HTTPException as e:
            log.error('%s:%s <%s> ' % (e.__class__.__name__,
                e.message, self.url))
        except SyncError as e:
            log.warning('%s' % e.message)


def main(**settings):
    base_url = settings['scielo_uri']
    resource = ((urljoin(base_url, 'books/'), 'book'),
        (urljoin(base_url, 'alphasum/'), 'alpha'),
        (urljoin(base_url, 'publishers/'), 'publisher'))

    # Create mongodb connection
    db_url = urlparse(settings['mongo_uri'])
    conn = pymongo.Connection(host=db_url.hostname, port=db_url.port)
    db = do_connect(conn, db_url)
    now = datetime.now()

    def run():
        jobs = []
        for src, dst in resource:
            j = Sync(src, dst, db)
            j.start()
            jobs.append(j)

        for job in jobs:
            job.join()

    run()
    db.catalog.save({'_id': 1, 'updated': now})


if __name__ == '__main__':
    import sys
    import ConfigParser
    import logging.config
    try:
        if len(sys.argv) < 3:
            print 'Usage: %s -f CONFIG_FILE'
            sys.exit(1)
        config = ConfigParser.RawConfigParser()
        config.readfp(open(sys.argv[-1]))
        settings = dict(config.items('app:main'))
        logging.config.fileConfig(sys.argv[-1])
        main(**settings)
    except IOError:
        print 'Usage: %s -f CONFIG_FILE'
        sys.exit(1)
