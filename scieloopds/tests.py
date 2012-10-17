import unittest
import feedparser
import json

from lxml import etree
from pyramid import testing


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
        self.assertEqual(entries[0]['_id'], 
			 'http://books.scielo.org/opds/new')
        self.assertEqual(entries[1]['_id'], 
			 'http://books.scielo.org/opds/publishers')
        self.assertEqual(entries[2]['_id'], 
			 'http://books.scielo.org/opds/alpha')

    def test_alpha(self):
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
            self.assertIn('links', entry)

class RendererTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_make_minimum_opds(self):
        from .renderers import make_entry
        mini_data = {'_id': u'1234', 'title':u'The War of the Worlds'}
        xml = make_entry(mini_data)
        feed = feedparser.parse(etree.tostring(xml))
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.title, u'The War of the Worlds')

    def test_make_opds_with_dc_elements(self):
        from .renderers import make_entry
        data = dict(_id=u'1234', language='pt-br', year='1963', 
		    title='The Title', isbn=u'123456', 
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
        data = dict(_id=u'1234', title=u'Test', content={'value': 'content'},
            updated=u'2012-10-14T18:16:01Z')
        xml = make_entry(data)
        feed = feedparser.parse(etree.tostring(xml))
        # bozo flag is 1 if feed is malformed; bozo == 0 if good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(u'content', entry.content[0]['value'])
        self.assertEqual(u'2012-10-14T18:16:01Z', entry.updated)

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
        self.assertTrue(entry.title.startswith(u'Compreendendo a complexidade'))
        self.assertEqual(u'EDUFBA', entry.publisher)


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
        self.assertEquals(u'http://books.scielo.org/opds/new', entries[0]['id'])
        link = entries[0]['links']
        self.assertEquals(1, len(link))
        self.assertEquals(u'/opds/new', link[0]['href'])
        # Publishers
        self.assertEquals(u'Publishers', entries[1]['title'])
        self.assertEquals(u'http://books.scielo.org/opds/publishers', entries[1]['id'])
        link = entries[1]['links']
        self.assertEquals(1, len(link))
        self.assertEquals(u'/opds/publishers', link[0]['href'])
        # Alphabetical
        self.assertEquals(u'Alphabetical', entries[2]['title'])
        self.assertEquals(u'http://books.scielo.org/opds/alpha', entries[2]['id'])
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
            self.assertTrue(entry['links'][0]['href'].startswith('/opds/alpha/'))
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
            self.assertTrue(entry['links'][0]['href'].startswith('/opds/publisher/'))
            self.assertEquals('subsection', entry['links'][0]['rel'])
            self.assertEquals(
                'application/atom+xml;profile=opds-catalog;kind=acquisition',
                entry['links'][0]['type'])
            self.assertIn('title', entry)

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
            self.assertIn('dc_identifier', entry)
            links = entry['links']
            self.assertTrue(links[0]['href'].startswith('/opds/book/'))
            # Complete Entry
            self.assertEquals('alternate', links[0]['rel'])           
            self.assertEquals(links[0]['type'],
                'application/atom+xml;profile=opds-catalog;kind=acquisition')
            # Acquisition PDF File
            self.assertEquals('http://opds-spec.org/acquisition', 
                links[1]['rel'])
            self.assertEquals(links[1]['type'], 'application/pdf')
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

    def test_alpha(self):
        from .models import Alphabetical
        for alpha in Alphabetical.filter():
            self.assertIn('_id', alpha)
            self.assertIn('title', alpha)
            self.assertIn('updated', alpha)

    def test_publisher(self):
        from .models import Publisher
        for pub in Publisher.filter():
            self.assertIn('_id', pub)
            self.assertIn('title', pub)
            self.assertIn('updated', pub)

    def test_book(self):
        from .models import Book
        books = Book.filter(limite=10)
        self.assertTrue(len(books) <= 10)
        for book in books:
            self.assertIn('_id', book)
            self.assertIn('title', book)
            self.assertIn('updated', book)
            self.assertIn('authors', book)
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