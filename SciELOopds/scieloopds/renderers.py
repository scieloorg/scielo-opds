
OPDS_CONTENT_TYPE = 'application/atom+xml; profile=opds-catalog; type=entry'

def opds_factory(info):
    def _render(value, system):
        request = system.get('request')
        if request is not None:
            response = request.response
            ct = response.content_type
            if ct == response.default_content_type:
                response.content_type = OPDS_CONTENT_TYPE
            response.charset = 'UTF-8'
        return MINIMUM_VALID_OPDS_ENTRY.format(**value)
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
