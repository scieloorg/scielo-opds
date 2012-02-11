import unittest

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

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from scieloopds import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/book/4321', status=200)
        self.assertTrue('/4321' in res.body)

