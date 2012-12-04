import math


class ContentType:
    CATALOG = 'application/atom+xml;profile=opds-catalog'
    NAVIGATION = 'application/atom+xml;profile=opds-catalog;kind=navigation'
    ACQUISITION = 'application/atom+xml;profile=opds-catalog;kind=acquisition'


class LinkRel:
    UP = 'up'
    SELF = 'self'
    FIRST = 'first'
    PREVIOUS = 'previous'
    NEXT = 'next'
    LAST = 'last'
    NEW = 'http://opds-spec.org/sort/new'
    SUBSECTION = 'subsection'
    ACQUISITION = 'http://opds-spec.org/acquisition'
    ALTERNATE = 'alternate'
    IMAGE = 'http://opds-spec.org/image'
    THUMBNAIL = 'http://opds-spec.org/image/thumbnail'


class Namespace:
    OPDS = 'http://opds-spec.org/2010/catalog'
    ATOM = 'http://www.w3.org/2005/Atom'


def make_link(rel, type, href):
    return {'rel': rel, 'type': type, 'href': href}


def make_pagination_links(base_url, current_page, items_per_page, total_items):
    links = []
    total_pages = math.ceil(total_items / float(items_per_page))

    if current_page < 0:
        current_page = 1

    if current_page > 1:
        links.append(make_link(LinkRel.FIRST, ContentType.ACQUISITION,
            '%s?page=%d' % (base_url, 1)))
        links.append(make_link(LinkRel.PREVIOUS, ContentType.ACQUISITION,
            '%s?page=%d' % (base_url, current_page - 1)))

    if current_page < total_pages:
        links.append(make_link(LinkRel.NEXT, ContentType.ACQUISITION,
            '%s?page=%d' % (base_url, current_page + 1)))
        links.append(make_link(LinkRel.LAST, ContentType.ACQUISITION,
            '%s?page=%d' % (base_url, total_pages)))

    return links