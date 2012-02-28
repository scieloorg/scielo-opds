from lxml import etree
from lxml.builder import ElementMaker # lxml only !

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
OPDS_NAMESPACE = 'http://opds-spec.org/2010/catalog'

OPDS_CONTENT_TYPE = 'application/atom+xml; profile=opds-catalog; type=entry'

def make_opds(**kwargs):
    # title, id, au_name, updated, link are mandatory
    atom = ElementMaker(namespace = ATOM_NAMESPACE,
                 nsmap={'atom' : ATOM_NAMESPACE})
    opds = ElementMaker(namespace = OPDS_NAMESPACE,
                 nsmap={'opds' : OPDS_NAMESPACE})

    atom_id = 'http://www.feedbooks.com/book/{id}'.format(**kwargs)
    xml = atom.entry(
        atom.title('The War of the Worlds'),
        atom.id('http://www.feedbooks.com/book/35'),
        atom.author(atom.name('H. G. Wells')
        ),
        atom.updated('2011-12-10T02:18:33Z'),
        atom.link(type='text/html', title='View on Feedbooks',
            href=atom_id, rel='alternate')
    )

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
        return make_opds(**value)
    return _render

MINIMUM_VALID_OPDS_ENTRY = u'''
<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom">
    <title>The War of the Worlds</title>
    <id>http://www.feedbooks.com/book/35</id>
    <author><name>H. G. Wells</name></author>
    <updated>2011-12-10T02:18:33Z</updated>
    <link type="text/html" title="View on Feedbooks"
          href="http://www.feedbooks.com/book/{id}" rel="alternate"/>
</entry>
'''.lstrip() # remove leading \n; <?xml...> declaration must be on line 1

# ODPS partial entry example from
# http://opds-spec.org/specs/opds-catalog-1-1-20110627/#Entry_Examples

PARTIAL_OPDS_ENTRY = u'''
<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:dc="http://purl.org/dc/elements/1.1/" >

    <title>Bob, Son of Bob</title>
    <id>urn:uuid:6409a00b-7bf2-405e-826c-3fdff0fd0734</id>
    <updated>2010-01-10T10:01:11Z</updated>
    <author>
        <name>Bob the Recursive</name>
        <uri>http://opds-spec.org/authors/1285</uri>
    </author>
    <dc:language>en</dc:language>
    <dc:issued>1917</dc:issued>
    <category scheme="http://www.bisg.org/standards/bisac_subject/index.html"
            term="FIC020000"
            label="FICTION / Men's Adventure"/>
    <summary type="text">The story of the son of the Bob and the gallant part he played in
                         the lives of a man and a woman.</summary>
    <link rel="http://opds-spec.org/image"     
        href="/covers/4561.lrg.png"
        type="image/png"/> 
    <link rel="http://opds-spec.org/image/thumbnail" 
          href="/covers/4561.thmb.gif"
          type="image/gif"/>

    <link rel="alternate"
          href="/opds-catalogs/entries/4571.complete.xml"
          type="application/atom+xml;type=entry;profile=opds-catalog" 
          title="Complete Catalog Entry for Bob, Son of Bob"/>

    <link rel="http://opds-spec.org/acquisition" 
          href="/content/free/4561.epub"
          type="application/epub+zip"/>
    <link rel="http://opds-spec.org/acquisition" 
          href="/content/free/4561.mobi"
          type="application/x-mobipocket-ebook"/>
</entry>
'''.lstrip() # remove leading \n; <?xml...> declaration must be on line 1

# ODPS complete entry example from
# http://opds-spec.org/specs/opds-catalog-1-1-20110627/#Entry_Examples

COMPLETE_OPDS_ENTRY = u'''
<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:dc="http://purl.org/dc/elements/1.1/" >

  <title>Bob, Son of Bob</title>
  <id>urn:uuid:6409a00b-7bf2-405e-826c-3fdff0fd0734</id>
  <updated>2010-01-10T10:01:11Z</updated>
 
  <author>
    <name>Bob the Recursive</name>
    <uri>http://opds-spec.org/authors/1285</uri>
  </author>
  <dc:language>en</dc:language>
  <dc:issued>1917</dc:issued>
  <category scheme="http://www.bisg.org/standards/bisac_subject/index.html"
            term="FIC020000"
            label="FICTION / Men's Adventure"/>
 
  <summary type="text">The story of the son of the Bob and the gallant part he played in
    the lives of a man and a woman.</summary>
  <content type="text">The story of the son of the Bob and the gallant part
    he played in the lives of a man and a woman. Bob begins his humble life
    under the wandering eye of his senile mother, but quickly learns how to
    escape into the wilder world. Follow Bob as he uncovers his father's past
    and uses those lessons to improve the lives of others.</content>
 
  <link rel="http://opds-spec.org/image"     
        href="/covers/4561.lrg.png"
        type="image/png"/> 
  <link rel="http://opds-spec.org/image/thumbnail" 
        href="/covers/4561.thmb.gif"
        type="image/gif"/>
 
  <link rel="self"
        href="/opds-catalogs/entries/4571.complete.xml"
        type="application/atom+xml;type=entry;profile=opds-catalog"/>
 
  <link rel="http://opds-spec.org/acquisition" 
        href="/content/free/4561.epub"
        type="application/epub+zip"/>
  <link rel="http://opds-spec.org/acquisition" 
        href="/content/free/4561.mobi"
        type="application/x-mobipocket-ebook"/>
</entry>
'''.lstrip() # remove leading \n; <?xml...> declaration must be on line 1

