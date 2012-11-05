import time
from opds import ContentType, Namespace, LinkRel
from lxml import etree
from lxml.builder import ElementMaker


def make_entry(values):
    """ Generate atom:entry from dict.
    """
    atom = ElementMaker(namespace=Namespace.ATOM,
        nsmap={'atom': Namespace.ATOM})
    dc = ElementMaker(namespace=Namespace.OPDS,
        nsmap={'dc': Namespace.OPDS})

    entry = atom.entry(
        atom.title(values['title']),
        atom.id(values['_id']))

    updated = values.get('updated', time.localtime())
    entry.append(atom.updated(time.strftime('%Y-%m-%dT%H:%M:%SZ', updated)))

    if 'language' in values:
        entry.append(dc.language(values['language']))

    if 'year' in values:
        entry.append(dc.issued(values['year']))

    if 'publisher' in values:
        entry.append(dc.publisher(values['publisher']))

    if 'eisbn' in values:
        entry.append(dc.identifier('urn:isbn:%s' % format(values['eisbn'])))

    links = values.get('links', [])
    for link in links:
        entry.append(atom.link(type=link['type'],
            href=link['href'], rel=link['rel']))

    if 'pdf_file' in values:
        link = values['pdf_file']
        entry.append(atom.link(type=link.get('type', 'application/pdf'),
            href=link['uri'], rel=LinkRel.ACQUISITION))

    if 'epub_file' in values:
        link = values['epub_file']
        entry.append(atom.link(type=link.get('type', 'application/epub+zip'),
            href=link['uri'], rel=LinkRel.ACQUISITION))

    if 'cover_thumbnail' in values:
        link = values['cover_thumbnail']
        entry.append(atom.link(type=link.get('type', 'image/jpeg'),
            href=link['uri'], rel=LinkRel.THUMBNAIL))

    if 'cover' in values:
        link = values['cover']
        entry.append(atom.link(type=link.get('type', 'image/jpeg'),
            href=link['uri'], rel=LinkRel.IMAGE))

    if 'content' in values:
        entry.append(atom.content(values['content']['value'],
            type=values['content'].get('type', 'text')))

    if 'synopsis' in values:
        entry.append(atom.summary(values['synopsis']))

    creators = values.get('creators', {})
    for author_key in ('individual_author', 'corporate_author', 'organizer'):
        for author in creators.get(author_key, []):
            new_author = atom.author(atom.name(author[0]))
            if author[1]:
                new_author.append(atom.uri(author[1]))
            entry.append(new_author)

    for contributor_key in ('editor', 'translator', 'collaborator', 'other',
        'coordinator'):
        for contributor in creators.get(contributor_key, []):
            new_contrib = atom.contributor(atom.name(contributor[0]))
            if contributor[1]:
                new_contrib.append(atom.uri(contributor[1]))
            entry.append(new_contrib)
    return entry


def make_feed(values):
    """ Generate atom:feed from dict.
    """
    atom = ElementMaker(namespace=Namespace.ATOM,
        nsmap={'atom': Namespace.ATOM})

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
        feed.append(atom.link(type=link['type'],
            href=link['href'], rel=link['rel']))

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
