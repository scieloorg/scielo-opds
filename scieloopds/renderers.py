import opds
from lxml import etree
from lxml.builder import ElementMaker

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'

def make_entry(values):
    """ Generate atom:entry from dict.
    """
    atom = ElementMaker(namespace = ATOM_NAMESPACE,
        nsmap =  {'atom' : ATOM_NAMESPACE})
    dc = ElementMaker(namespace = opds.NAMESPACE,
        nsmap={'dc' : opds.NAMESPACE})

    entry = atom.entry(
        atom.title(values['title']),
        atom.id(values['_id'])
    )

    if values.has_key('updated'):
        entry.append(atom.updated(values['updated']))

    if values.has_key('language'):
        entry.append(dc.language(values['language']))

    if values.has_key('year'):
        entry.append(dc.issued(values['year']))

    links = values.get('links', [])
    for link in links:
        entry.append(atom.link(type = link['type'], 
            href = link['href'], rel = link['rel']))

    if values.has_key('content'):
        entry.append(atom.content(values['content'], type = 'xhtml'))

    return entry


def make_feed(values):
    """ Generate atom:feed from dict.
    """
    atom = ElementMaker(namespace = ATOM_NAMESPACE,
        nsmap =  {'atom' : ATOM_NAMESPACE})

    feed = atom.feed(
        atom.id(values.get('_id', u'http://books.scielo.org/opds/')),
        atom.title(values.get('title', u'SciELO Books')),
        atom.updated(u'2012-10-04T21:26:04Z'),
        atom.author(
            atom.name(u'SciELO Books'),
            atom.uri(u'http://books.scielo.org'),
            atom.email(u'scielo.books@scielo.org')
        ),
        atom.link(type=opds.NAVIGATION, 
            href=u'/opds/', rel=u'start')
    )

    links = values.get('links', [])
    for link in links:
        feed.append(atom.link(type = link['type'], 
            href = link['href'], rel = link['rel']))

    entries = values.get('entry', [])
    for entry_values in entries:
        feed.append(make_entry(entry_values))

    return feed


def opds_factory(info):
    """ Pyramid Render which return OPDS Feed
    """
    def _render(value, system):
        request = system.get('request')
        if request is not None:
            response = request.response
            response.charset = 'UTF-8'
            response.content_type = opds.CATALOG
        return etree.tostring(make_feed(value), pretty_print=True)
    return _render
