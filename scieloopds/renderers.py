import time
from opds import ContentType, Namespace, LinkRel
from lxml import etree
from lxml.builder import ElementMaker

def make_entry(values):
    """ Generate atom:entry from dict.
    """
    atom = ElementMaker(namespace = Namespace.ATOM,
        nsmap =  {'atom' : Namespace.ATOM})
    dc = ElementMaker(namespace = Namespace.OPDS,
        nsmap={'dc' : Namespace.OPDS})

    entry = atom.entry(
        atom.title(values['title']),
        atom.id(values['_id'])
    )

    updated = values.get('updated', time.localtime())
    entry.append(atom.updated(time.strftime('%Y-%m-%dT%H:%M:%SZ', updated)))

    if values.has_key('language'):
        entry.append(dc.language(values['language']))

    if values.has_key('year'):
        entry.append(dc.issued(values['year']))

    if values.has_key('publisher'):
        entry.append(dc.publisher(values['publisher']))

    if values.has_key('isbn'):
        entry.append(dc.identifier('urn:isbn:%s' % format(values['isbn'])))

    links = values.get('links', [])
    for link in links:
        entry.append(atom.link(type = link['type'], 
            href = link['href'], rel = link['rel']))

    if values.has_key('pdf_file'):
        link = values['pdf_file']
        entry.append(atom.link(type = link.get('type', 'application/pdf'),
            href = link['uri'], rel = LinkRel.ACQUISITION))

    if values.has_key('epub_file'):
        link = values['epub_file']
        entry.append(atom.link(type = link.get('type', 'application/epub+zip'),
            href = link['uri'], rel = LinkRel.ACQUISITION))

    if values.has_key('cover_thumbnail'):
        link = values['cover_thumbnail']
        entry.append(atom.link(type = link.get('type', 'image/jpeg'),
            href = link['uri'], rel = LinkRel.THUMBNAIL))

    if values.has_key('cover'):
        link = values['cover']
        entry.append(atom.link(type = link.get('type', 'image/jpeg'),
            href = link['uri'], rel = LinkRel.IMAGE))

    if values.has_key('content'):
        entry.append(atom.content(values['content']['value'],
            type = values['content'].get('type', 'text')))

    if values.has_key('synopsis'):
        entry.append(atom.summary(values['synopsis']))

    authors = values.get('authors', [])
    for author_values in authors:
        author = atom.author(atom.name(author_values['name']))

        resume = author_values.get('uri', None)
        if resume: author.append(atom.uri(resume))
        
        email = author_values.get('email', None)
        if email: author.append(atom.email(email))

        entry.append(author)

    contributors = values.get('contributors', [])
    for contributor_values in authors:
        contributor = atom.author(atom.name(contributor_values['name']))

        uri = contributor_values.get('uri', None)
        if uri: author.append(atom.uri(uri))
        
        email = contributor_values.get('email', None)
        if email: author.append(atom.email(email))

        entry.append(contributor)

    return entry


def make_feed(values):
    """ Generate atom:feed from dict.
    """
    atom = ElementMaker(namespace = Namespace.ATOM,
        nsmap =  {'atom' : Namespace.ATOM})

    updated = values.get('updated', time.localtime())

    feed = atom.feed(
        atom.id(values.get('_id', u'http://books.scielo.org/opds/')),
        atom.title(values.get('title', u'SciELO Books')),
        atom.updated(time.strftime('%Y-%m-%dT%H:%M:%SZ', updated)),
        atom.author(
            atom.name(u'SciELO Books'),
            atom.uri(u'http://books.scielo.org'),
            atom.email(u'scielo.books@scielo.org')
        ),
        atom.link(type=ContentType.NAVIGATION, 
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
            response.charset = 'utf-8'
            response.content_type = ContentType.CATALOG
        return etree.tostring(make_feed(value), pretty_print=True)
    return _render
