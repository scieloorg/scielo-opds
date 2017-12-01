# coding: utf-8
"""
.. module: scieloopds.urllib2_mock
   :synopsis: Mock utilities for automated tests.

.. moduleauthor:: Allison Vollmann <allisonvoll@gmail.com>
"""
from urllib2 import HTTPError

_match = {
    'http://books.scielo.org/api/v1/publishers/': 'publishers_list.json',
    'http://books.scielo.org/api/v1/alphasum/': 'alpha_sum.json',
    'http://books.scielo.org/api/v1/books/': '37t.json'}


class Request(object):
    def __init__(self, url, data=None):
        self.url = url

    def get_full_url(self):
        return self.url


def urlopen(request):
    res = _match.get(request.get_full_url().split('?')[0])
    if not res:
        raise HTTPError(request.get_full_url(), 404, '', '', None)
    return open('%s/%s/%s' % (__package__, 'fixtures', res))
