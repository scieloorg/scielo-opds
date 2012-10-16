class ContentType:
    CATALOG = 'application/atom+xml;profile=opds-catalog'
    NAVIGATION = u'application/atom+xml;profile=opds-catalog;kind=navigation'
    ACQUISITION = u'application/atom+xml;profile=opds-catalog;kind=acquisition'

class LinkRel:
    NEW = u'http://opds-spec.org/sort/new'
    SUBSECTION = u'subsection'
    ACQUISITION = u'http://opds-spec.org/acquisition'
    ALTERNATE = u'alternate'
    IMAGE = u'http://opds-spec.org/image'
    THUMBNAIL = u'http://opds-spec.org/image/thumbnail'

class Namespace:
    OPDS = u'http://opds-spec.org/2010/catalog'
    ATOM = u'http://www.w3.org/2005/Atom'