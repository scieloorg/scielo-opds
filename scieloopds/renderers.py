from lxml import etree
from lxml.builder import ElementMaker

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
OPDS_NAMESPACE = 'http://opds-spec.org/2010/catalog'

class OpdsFeed(object):

	def __init__(self, values):
		self.atom = ElementMaker(namespace = ATOM_NAMESPACE,
			nsmap =  {'atom' : ATOM_NAMESPACE})
		self.dc = ElementMaker(namespace = OPDS_NAMESPACE,
			nsmap={'dc' : OPDS_NAMESPACE})
		self._make_feed(values)

	def __str__(self):
		return etree.tostring(self.feed, pretty_print=True)

	def _make_feed(self, values):
		self.feed = self.atom.feed(
			self.atom.id(values.pop('id')),
			self.atom.title(values.pop('title')),
			self.atom.updated(values.pop('updated'))
		)
		
		self.feed.append(self._make_author(values.pop('author')))

		links = values.pop('link')

		for link in links:
			self.feed.append(self._make_link(link))		

		entries = values.pop('entry')
		for entry in entries:
			self.feed.append(self._make_entry(entry))

	def _make_author(self, values):
		author = self.atom.author()
		author.append(self.atom.name(values.pop('name')))

		if values.has_key('uri'):
			author.append(self.atom.uri(values.pop('uri')))

		if values.has_key('email'):
			author.append(self.atom.email(values.pop('email')))

		return author
		
	def _make_entry(self, values):
		entry = self.atom.entry(
			self.atom.title(values.pop('title')),
			self.atom.id(values.pop('id')),
			self.atom.updated(values.pop('updated'))
		)

		if values.has_key('author'):
			entry.append(self._make_author(values.pop('author')))

		links = values.pop('link')

		for link in links:
			entry.append(self._make_link(link))

		return entry

	def _make_link(self, values):
		link = self.atom.link(
			type  = values.pop('type'),
			href  = values.pop('href'), 
			rel   = values.pop('rel'))
		return link

def opds_factory(info):
	def _render(value, system):
		request = system.get('request')
		if request is not None:
			response = request.response
			response.charset = 'UTF-8'
		return str(OpdsFeed(value))
	return _render