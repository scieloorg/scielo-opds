# coding: utf-8
"""
.. module: scieloopds.opds
   :synopsis: Useful utilities to help build OPDS catalog.

.. moduleauthor:: Allison Vollmann <allisonvoll@gmail.com>
"""

import math


class ContentType:
    """Document content type"""
    CATALOG = 'application/atom+xml;profile=opds-catalog'
    NAVIGATION = 'application/atom+xml;profile=opds-catalog;kind=navigation'
    ACQUISITION = 'application/atom+xml;profile=opds-catalog;kind=acquisition'


class LinkRel:
    """OPDS (Atom) link relation"""
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
    """XML documment namespaces"""
    OPDS = 'http://opds-spec.org/2010/catalog'
    ATOM = 'http://www.w3.org/2005/Atom'


def make_link(rel, type, href):
    """Create an OPDS (Atom) link as dict

    :param rel: Link relation (LinkRel.Acquisition, LinkRel.Alternate...).
    :type rel: opds.LinkRel.
    :param type: Content type of the link destination.
    :type state: opds.ContentType.
    :param href: Link destination url.
    :type href: str.
    :returns: dict.
    """
    return {'rel': rel, 'type': type, 'href': href}


def make_pagination_links(base_url, current_page, items_per_page, total_items):
    """Creta OPDS (Atom) links for catalog pagination

    :param base_url: URL of resource which will be paginated.
    :type base_url: str.
    :param current_page: Number of actual page.
    :type current_page: int.
    :param items_per_page: Entries that will be displayed on each page.
    :type items_per_page: int.
    :param total_items: Total entries.
    :type total_items: int.
    :returns:  list.
    """
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
