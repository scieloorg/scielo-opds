import unittest
import feedparser
import json
import sync
import urllib2_mock
from datetime import datetime

from lxml import etree
from pyramid import testing


def setUpModule():
    from models import Mongo
    sync.urllib2 = urllib2_mock
    Mongo.get_collection('alpha').drop()
    Mongo.get_collection('publisher').drop()
    Mongo.get_collection('book').drop()
    sync.main()


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_root(self):
        from .views import root
        request = testing.DummyRequest()
        info = root(request)
        entries = info['entry']
        self.assertEqual('http://books.scielo.org/opds/new',
            entries[0]['_id'])
        self.assertEqual('http://books.scielo.org/opds/publisher',
            entries[1]['_id'])
        self.assertEqual('http://books.scielo.org/opds/alpha',
            entries[2]['_id'])

    def test_alpha_catalog(self):
        from .views import alpha_catalog
        request = testing.DummyRequest()
        info = alpha_catalog(request)
        self.assertIn('_id', info)
        self.assertIn('title', info)
        self.assertIn('links', info)
        self.assertIn('entry', info)

        entries = info['entry']
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('title', entry)
            self.assertIn('updated', entry)
            self.assertIn('links', entry)

    def test_alpha_filter(self):
        from .views import alpha_filter
        request = testing.DummyRequest()
        request.matchdict['id'] = 'c'
        info = alpha_filter(request)
        self.assertIn('_id', info)
        self.assertIn('title', info)
        self.assertIn('links', info)
        self.assertIn('entry', info)

        entries = info['entry']
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('title', entry)
            self.assertIn('updated', entry)
            self.assertIn('cover', entry)
            self.assertIn('cover_thumbnail', entry)
            self.assertIn('pdf_file', entry)
            self.assertIn('epub_file', entry)
            self.assertTrue(entry['title'].startswith(u'C'))

    def test_publishers(self):
        from .views import publisher_catalog
        request = testing.DummyRequest()
        info = publisher_catalog(request)
        self.assertIn('_id', info)
        self.assertIn('title', info)
        self.assertIn('links', info)
        self.assertIn('entry', info)

        entries = info['entry']
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('title', entry)
            self.assertIn('updated', entry)
            self.assertIn('links', entry)

    def test_publisher_filter(self):
        from .views import publisher_filter
        request = testing.DummyRequest()
        request.matchdict['id'] = 'edufba'
        info = publisher_filter(request)
        self.assertIn('_id', info)
        self.assertIn('title', info)
        self.assertIn('links', info)
        self.assertIn('entry', info)

        entries = info['entry']
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('title', entry)
            self.assertIn('updated', entry)
            self.assertIn('cover', entry)
            self.assertIn('cover_thumbnail', entry)
            self.assertIn('pdf_file', entry)
            self.assertIn('epub_file', entry)
            self.assertEquals(u'EDUFBA', entry['publisher'])

    @unittest.skip("Implement new releases in mongo backend")
    def test_new(self):
        from .views import new
        request = testing.DummyRequest()
        info = new(request)
        self.assertIn('_id', info)
        self.assertIn('title', info)
        self.assertIn('links', info)
        self.assertIn('entry', info)

        entries = info['entry']
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('title', entry)
            self.assertIn('updated', entry)
            self.assertIn('cover', entry)
            self.assertIn('cover_thumbnail', entry)
            self.assertIn('pdf_file', entry)
            self.assertIn('epub_file', entry)


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_make_minimum_opds(self):
        from .renderers import make_entry
        mini_data = {'_id': u'1234', 'title': u'The War of the Worlds'}
        xml = make_entry(mini_data)
        feed = feedparser.parse(etree.tostring(xml))
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.title, u'The War of the Worlds')

    def test_make_opds_with_dc_elements(self):
        from .renderers import make_entry
        data = dict(_id=u'1234', language='pt-br', year='1963',
            title='The Title', eisbn=u'123456',
            publisher=u'publisher')
        xml = make_entry(data)
        feed = feedparser.parse(etree.tostring(xml))
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.language, u'pt-br')
        self.assertEqual(entry.dc_issued, u'1963')
        self.assertEqual(entry.dc_identifier, u'urn:isbn:123456')
        self.assertEqual(entry.publisher, u'publisher')

    def test_make_opds_with_atom_elements(self):
        from .renderers import make_entry
        updated = datetime.now()
        data = dict(_id=u'1234', title=u'Test', content={'value': 'content'},
            updated=updated)
        xml = make_entry(data)
        feed = feedparser.parse(etree.tostring(xml))
        # bozo flag is 1 if feed is malformed; bozo == 0 if good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(u'content', entry.content[0]['value'])
        self.assertEqual(updated.strftime('%Y-%m-%dT%H:%M:%SZ'),
            entry.updated)

    def test_make_opds_from_scielobooks_monograph_large(self):
        # the largest monograph JSON record as of feb/2012
        book_data = json.load(open('scieloopds/fixtures/37t.json'))
        from .renderers import make_entry
        xml = make_entry(book_data[0])
        feed = feedparser.parse(etree.tostring(xml))
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.language, u'pt')
        self.assertEqual(entry.dc_issued, u'2009')
        self.assertTrue(
            entry.title.startswith(u'Compreendendo a complexidade'))
        self.assertEqual(u'EDUFBA', entry.publisher)
        self.assertEqual(u'urn:isbn:9788523205607', entry.dc_identifier)
        self.assertEqual(u'Ribeiro, Maria Teresa Franco', entry.author)
        self.assertEqual(u'Milani, Carlos Roberto Sanchez',
            entry.contributors[0].name)

    def test_make_opds_with_author_contributor(self):
        data = dict(_id='1234', title=u'Test')
        creators = dict()
        authors = (u'organizer', u'individual', u'corporate')
        contributors = (u'translator', u'coordinator', u'collaborator',
            u'editor', u'other')
        creators['organizer'] = [[authors[0], None], ]
        creators['individual_author'] = [[authors[1], u'uri'], ]
        creators['corporate_author'] = [[authors[2], u'uri'], ]
        creators['translator'] = [[contributors[0], None], ]
        creators['coordinator'] = [[contributors[1], u'uri'], ]
        creators['collaborator'] = [[contributors[2], u'uri'], ]
        creators['editor'] = [[contributors[3], None], ]
        creators['other'] = [[contributors[4], u'uri'], ]
        data['creators'] = creators
        from .renderers import make_entry
        xml = make_entry(data)
        feed = feedparser.parse(etree.tostring(xml))
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)

        entry = feed.entries[0]
        count = 0
        for author in entry.authors:
            self.assertIn(author.name, authors)
            if hasattr(author, 'href'):
                self.assertEquals(author.href, 'uri')
                count += 1
        # 2 authors with uri
        self.assertEquals(count, 2)

        count = 0
        for contrib in entry.contributors:
            self.assertIn(contrib.name, contributors)
            if hasattr(contrib, 'href'):
                self.assertEquals(contrib.href, 'uri')
                count += 1
        # 2 contributors with uri
        self.assertEquals(count, 3)


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from scieloopds import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/opds/', status=200)
        ct = res.content_type
        # check for the right content type
        self.assertTrue(ct.startswith('application/atom+xml'))
        # bozo flag is 1 if feed is malformed; bozo == 0 is goot
        feed = feedparser.parse(res.body)
        self.assertFalse(feed.bozo)
        # catalog root must have links with rel=(start, self)
        self.assertEquals(2, len(feed.feed.links))
        self.assertEquals('start', feed.feed.links[0]['rel'])
        self.assertEquals('/opds/', feed.feed.links[0]['href'])
        self.assertEquals('self', feed.feed.links[1]['rel'])
        self.assertEquals('/opds/', feed.feed.links[1]['href'])
        # check for catalog root entries
        # New Releases
        entries = feed.entries
        self.assertEquals(3, len(entries))
        self.assertEquals(u'New Releases', entries[0]['title'])
        self.assertEquals(u'http://books.scielo.org/opds/new',
            entries[0]['id'])
        link = entries[0]['links']
        self.assertEquals(1, len(link))
        self.assertEquals(u'/opds/new', link[0]['href'])
        # Publishers
        self.assertEquals(u'Publishers', entries[1]['title'])
        self.assertEquals(u'http://books.scielo.org/opds/publisher',
            entries[1]['id'])
        link = entries[1]['links']
        self.assertEquals(1, len(link))
        self.assertEquals(u'/opds/publisher', link[0]['href'])
        # Alphabetical
        self.assertEquals(u'Alphabetical', entries[2]['title'])
        self.assertEquals(u'http://books.scielo.org/opds/alpha',
            entries[2]['id'])
        link = entries[2]['links']
        self.assertEquals(1, len(link))
        self.assertEquals(u'/opds/alpha', link[0]['href'])

    def test_alpha_catalog(self):
        res = self.testapp.get('/opds/alpha', status=200)
        ct = res.content_type
        # check for the right content type
        self.assertTrue(ct.startswith('application/atom+xml'))
        # bozo flag is 1 if feed is malformed; bozo == 0 is goot
        feed = feedparser.parse(res.body)
        self.assertFalse(feed.bozo)
        # alpha catalog must have links with rel=(self, start, up)
        self.assertEquals(3, len(feed.feed.links))
        self.assertEquals('start', feed.feed.links[0]['rel'])
        self.assertEquals('/opds/', feed.feed.links[0]['href'])
        self.assertEquals('up', feed.feed.links[1]['rel'])
        self.assertEquals('/opds/', feed.feed.links[1]['href'])
        self.assertEquals('self', feed.feed.links[2]['rel'])
        self.assertEquals('/opds/alpha', feed.feed.links[2]['href'])
        # check for catalog entries
        entries = feed.entries
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('links', entry)
            self.assertTrue(entry['links'][0]['href'].
                startswith('/opds/alpha/'))
            self.assertEquals('subsection', entry['links'][0]['rel'])
            self.assertEquals(
                'application/atom+xml;profile=opds-catalog;kind=acquisition',
                entry['links'][0]['type'])
            self.assertIn('title', entry)

    def test_publisher_catalog(self):
        res = self.testapp.get('/opds/publisher', status=200)
        ct = res.content_type
        # check for the right content type
        self.assertTrue(ct.startswith('application/atom+xml'))
        # bozo flag is 1 if feed is malformed; bozo == 0 is goot
        feed = feedparser.parse(res.body)
        self.assertFalse(feed.bozo)
        # alpha catalog must have links with rel=(self, start, up)
        self.assertEquals(3, len(feed.feed.links))
        self.assertEquals('start', feed.feed.links[0]['rel'])
        self.assertEquals('/opds/', feed.feed.links[0]['href'])
        self.assertEquals('up', feed.feed.links[1]['rel'])
        self.assertEquals('/opds/', feed.feed.links[1]['href'])
        self.assertEquals('self', feed.feed.links[2]['rel'])
        self.assertEquals('/opds/publisher', feed.feed.links[2]['href'])
        # check for catalog entries
        entries = feed.entries
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('links', entry)
            self.assertTrue(entry['links'][0]['href'].
                startswith('/opds/publisher/'))
            self.assertEquals('subsection', entry['links'][0]['rel'])
            self.assertEquals(
                'application/atom+xml;profile=opds-catalog;kind=acquisition',
                entry['links'][0]['type'])
            self.assertIn('title', entry)

    @unittest.skip("Implement new releases in mongo backend")
    def test_new(self):
        res = self.testapp.get('/opds/new', status=200)
        ct = res.content_type
        # check for the right content type
        self.assertTrue(ct.startswith('application/atom+xml'))
        # bozo flag is 1 if feed is malformed; bozo == 0 is goot
        feed = feedparser.parse(res.body)
        self.assertFalse(feed.bozo)
        # new catalog must have links with rel=(self, start, up)
        self.assertEquals(3, len(feed.feed.links))
        self.assertEquals('start', feed.feed.links[0]['rel'])
        self.assertEquals('/opds/', feed.feed.links[0]['href'])
        self.assertEquals('up', feed.feed.links[1]['rel'])
        self.assertEquals('/opds/', feed.feed.links[1]['href'])
        self.assertEquals('self', feed.feed.links[2]['rel'])
        self.assertEquals('/opds/new', feed.feed.links[2]['href'])
        # check for catalog entries
        entries = feed.entries
        self.assertTrue(len(entries) > 0)
        for entry in entries:
            self.assertIn('links', entry)
            self.assertIn('title', entry)
            self.assertIn('updated', entry)
            self.assertIn('publisher', entry)
            links = entry['links']
            # Acquisition PDF File
            self.assertEquals('http://opds-spec.org/acquisition',
                links[0]['rel'])
            self.assertEquals(links[0]['type'], 'application/pdf')
            # Acquisition Epub File
            self.assertEquals('http://opds-spec.org/acquisition',
                links[1]['rel'])
            self.assertEquals(links[1]['type'], 'application/epub+zip')
            # Thumbnail Image
            self.assertEquals('http://opds-spec.org/image/thumbnail',
                links[2]['rel'])
            self.assertEquals(links[2]['type'], 'image/jpeg')
            # Cover Image
            self.assertEquals('http://opds-spec.org/image',
                links[3]['rel'])
            self.assertEquals(links[3]['type'], 'image/jpeg')


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_catalog_alpha(self):
        from .models import Catalog
        catalog = Catalog.get('alpha')
        self.assertEquals('alpha', catalog['_id'])
        self.assertIn('updated', catalog)
        self.assertIsInstance(catalog['updated'], datetime)
        for alpha in catalog['entry']:
            self.assertIn('_id', alpha)
            self.assertIn('title', alpha)
            self.assertIn('updated', alpha)
            self.assertIsInstance(alpha['updated'], datetime)
            self.assertIn('content', alpha)
            self.assertIn('links', alpha)

    def test_filter_alpha(self):
        from .models import Alphabetical
        alpha = Alphabetical.get('c')
        self.assertEquals('c', alpha['_id'])
        self.assertIn('updated', alpha)
        self.assertIsInstance(alpha['updated'], datetime)
        for entry in alpha['entry']:
            self.assertIn('_id', entry)
            self.assertIn('title', entry)
            self.assertIn('updated', entry)
            self.assertIsInstance(entry['updated'], datetime)
            self.assertIn('publisher', entry)
            self.assertIn('title', entry)

    def test_catalog_publisher(self):
        from .models import Catalog
        catalog = Catalog.get('publisher')
        self.assertEquals('publisher', catalog['_id'])
        self.assertIn('updated', catalog)
        self.assertIsInstance(catalog['updated'], datetime)
        for pub in catalog['entry']:
            self.assertIn('_id', pub)
            self.assertIn('title', pub)
            self.assertIn('updated', pub)
            self.assertIsInstance(pub['updated'], datetime)
            self.assertIn('content', pub)
            self.assertIn('links', pub)

    @unittest.skip("Implement new releases in mongo backend")
    def test_book(self):
        from .models import Book
        books = Book.filter()
        for book in books:
            self.assertIn('_id', book)
            self.assertIn('title', book)
            self.assertIn('cover', book)
            self.assertIn('cover_thumbnail', book)


class OpdsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_make_link(self):
        from .opds import make_link
        link = make_link('http://opds-spec.org/image', 'image/jpeg',
            'http://test.tld/img.jpg')
        self.assertEquals('http://opds-spec.org/image', link['rel'])
        self.assertEquals('image/jpeg', link['type'])
        self.assertEquals('http://test.tld/img.jpg', link['href'])