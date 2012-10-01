from opds import *
from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project':'scielo-opds'}

class OpdsView(object):
	def __init__(self, request):
		self.request = request
		self.request.response.content_type = OPDS_CATALOG
		self.url = request.host_url
		self.record = {
			'title' : u'SciELO Books',
			'id' : '{0}/opds'.format(self.url),
			'author' : {
				'name': u'SciELO Books',
				'uri': u'http://books.scielo.org/',
				'email': u'scielo.books@scielo.org'
			},
			'updated' : '2012-09-29T18:24:01Z',
			'link' : ({
					'rel' : 'self', 
					'href' : '/opds/', 
					'type' : OPDS_NAVIGATION},
				{
					'rel' : 'start', 
					'href' : '/opds/', 
					'type' : OPDS_NAVIGATION})
			}

	@view_config(route_name='root', renderer='opds')
	def root(self):
		entry = []
		entry.append({
			'id': '{0}/opds/new'.format(self.url), 
			'title' : 'New Releases', 
			'updated' : '2012-09-29T19:27:01Z',
			'link' : ({
				'rel' : OPDS_NEW,
				'href' : '/opds/new',
				'type' : OPDS_ACQUISITION},)
			})
		entry.append({
			'id': '{0}/opds/publishers'.format(self.url), 
			'title' : 'Publishers', 
			'updated' : '2012-09-29T19:27:01Z',
			'link' : ({
				'rel' : OPDS_SUBSECTION,
				'href' : '/opds/publishers',
				'type' : OPDS_NAVIGATION},)
			})
		entry.append({
			'id': '{0}/opds/alpha'.format(self.url), 
			'title' : 'Alphabetical', 
			'updated' : '2012-09-29T19:27:01Z',
			'link' : ({
				'rel' : OPDS_SUBSECTION,
				'href' : '/opds/new',
				'type' : OPDS_NAVIGATION},)
			})
		self.record['entry'] = tuple(entry)

		return self.record