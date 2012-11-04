class ContentType:
    CATALOG = 'application/atom+xml;profile=opds-catalog'
    NAVIGATION = 'application/atom+xml;profile=opds-catalog;kind=navigation'
    ACQUISITION = 'application/atom+xml;profile=opds-catalog;kind=acquisition'


class LinkRel:
    UP = 'up'
    SELF = 'self'
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