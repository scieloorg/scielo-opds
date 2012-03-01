import unittest
import feedparser
import json

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'SciELOopds')

    def test_full_entry(self):
        from .views import full_entry
        request = testing.DummyRequest(matchdict={'id':'1234'})
        info = full_entry(request)
        self.assertEqual(info['_id'], '1234')

class RendererTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_make_minimum_opds(self):
        from .renderers import make_opds
        mini_data = {'_id':1234, 'title':u'The War of the Worlds'}
        xml = make_opds(mini_data)
        feed = feedparser.parse(xml)
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.title, u'The War of the Worlds')

    def test_make_opds_with_dc_elements(self):
        from .renderers import make_opds
        data = dict(_id=1234, language='pt-br', year='1963', title='The Title')
        xml = make_opds(data)
        feed = feedparser.parse(xml)
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.language, u'pt-br')
        self.assertEqual(entry.dc_issued, u'1963')

    def test_make_opds_from_scielobooks_monograph_large(self):
        # the largest monograph JSON record as of feb/2012
        book_data = json.load(open('scieloopds/fixtures/37t.json'))
        from .renderers import make_opds
        xml = make_opds(book_data)
        feed = feedparser.parse(xml)
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.language, u'pt')
        self.assertEqual(entry.dc_issued, u'2009')
        self.assertTrue(entry.title.startswith(u'Compreendendo a complexidade'))


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_link_class(self):
        from .models import Link
        link = Link(href='/content/free/4561.epub',
                    rel='http://opds-spec.org/acquisition',
                    type='application/epub+zip')
        self.assertEqual(link.as_dict(), {'rel':"http://opds-spec.org/acquisition",
                                     'href':"/content/free/4561.epub",
                                     'type':"application/epub+zip"})

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from scieloopds import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/book/4321', status=200)
        self.assertTrue('/4321' in res.body)

