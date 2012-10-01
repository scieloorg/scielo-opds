import unittest
import feedparser
from pyramid import testing
from opds import *

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'scielo-opds')

class FunctionalTests(unittest.TestCase):
	def setUp(self):		
		from scieloopds import main
		from webtest import TestApp		
		self.config = testing.setUp()
		self.testapp = TestApp(main({}))

	def tearDown(self):
		testing.tearDown()

	def test_root(self):
		res = self.testapp.get('/opds/', status=200)
		f = feedparser.parse(res.body)		
		self.assertFalse(f.bozo)
		
		links = f.feed.links
		self.assertEqual(u'self', links[0]['rel'])
		self.assertEqual(u'/opds/', links[0]['href'])
		self.assertEqual(OPDS_NAVIGATION, links[0]['type'])

		self.assertEqual(u'start', links[1]['rel'])
		self.assertEqual(u'/opds/', links[0]['href'])
		self.assertEqual(OPDS_NAVIGATION, links[0]['type'])