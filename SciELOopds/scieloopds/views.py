from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project':'SciELOopds'}
    
@view_config(route_name='full_entry', renderer='opds')
def full_entry(request):
    request.response.content_type = 'text/xml'
    return {'id':request.matchdict['id']}
