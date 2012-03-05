from lxml import etree
from lxml.builder import ElementMaker # lxml only !

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
OPDS_NAMESPACE = 'http://opds-spec.org/2010/catalog'

OPDS_CONTENT_TYPE = 'application/atom+xml; profile=opds-catalog; type=entry'

def make_opds(monograph_dict):
    # title, id, au_name, updated, link are mandatory
    atom = ElementMaker(namespace = ATOM_NAMESPACE,
                 nsmap={'atom' : ATOM_NAMESPACE})
    dc = ElementMaker(namespace = OPDS_NAMESPACE,
                 nsmap={'dc' : OPDS_NAMESPACE})

    atom_id = 'http://www.feedbooks.com/book/{_id}'.format(**monograph_dict)
    xml = atom.entry(
        atom.title(monograph_dict['title']),
        atom.id('http://www.feedbooks.com/book/35'),
        atom.author(atom.name('H. G. Wells')
        ),
        atom.updated('2011-12-10T02:18:33Z'),
        atom.link(type='text/html', title='View on Feedbooks',
            href=atom_id, rel='alternate')
    )
    if 'language' in monograph_dict:
        xml.append(dc.language(monograph_dict['language']))
    if 'year' in monograph_dict:
        xml.append(dc.issued(monograph_dict['year']))

    return etree.tostring(xml, pretty_print=True)

def opds_factory(info):
    def _render(value, system):
        request = system.get('request')
        if request is not None:
            response = request.response
            ct = response.content_type
            if ct == response.default_content_type:
                response.content_type = OPDS_CONTENT_TYPE
            response.charset = 'UTF-8'
        #return MINIMUM_VALID_OPDS_ENTRY.format(**value)
        return make_opds(value)
    return _render

