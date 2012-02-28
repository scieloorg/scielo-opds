import unittest
import feedparser

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
        self.assertEqual(info['id'], '1234')

class RendererTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_make_minimum_opds(self):
        from .renderers import make_opds
        mini_data = {'id':1234}
        xml = make_opds(**mini_data)
        feed = feedparser.parse(xml)
        # bozo flag is 1 if feed is malformed; bozo == 0 is good
        self.assertFalse(feed.bozo)
        entry = feed.entries[0]
        self.assertEqual(entry.title, u'The War of the Worlds')

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

