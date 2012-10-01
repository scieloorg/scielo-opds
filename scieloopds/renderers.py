import opds
from lxml import etree
from lxml.builder import ElementMaker

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'

def make_feed(values):
    atom = ElementMaker(namespace = ATOM_NAMESPACE,
        nsmap =  {'atom' : ATOM_NAMESPACE})
    dc = ElementMaker(namespace = opds.NAMESPACE,
        nsmap={'dc' : opds.NAMESPACE})

    feed = atom.feed(
        atom.id(u'http://books.scielo.org/opds/'),
        atom.title(u'SciELO Books'),
        atom.updated(u'2012-10-04T21:26:04Z'),
        atom.author(
            atom.name(u'SciELO Books'),
            atom.uri(u'http://books.scielo.org'),
            atom.email(u'scielo.books@scielo.org')
        ),
        atom.link(type=opds.NAVIGATION, 
            href=u'/opds/', rel=u'start')
    )

    links = values.get('link', [])
    for link in links:
        feed.append(atom.link(type = link['type'], 
            href = link['href'], rel = link['rel']))

    entries = values.get('entry', [])
    for entry in entries:
        new_entry = atom.entry(
            atom.title(entry['title']),
            atom.id(entry['id']),
            atom.updated(entry['updated'])
        )

        #TODO(allisonvoll@gmail.com): Implement author tag

        links = entry['link']
        for link in links:
            new_entry.append(atom.link(type = link['type'], 
                href = link['href'], rel = link['rel']))

        feed.append(new_entry)
    return etree.tostring(feed, pretty_print=True)

def opds_factory(info):
    def _render(value, system):
        request = system.get('request')
        if request is not None:
            response = request.response
            response.charset = 'UTF-8'
            response.content_type = opds.CATALOG
        return make_feed(value)
    return _render
