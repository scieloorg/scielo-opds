from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')    
    config.add_route('root', 'opds/')
    #TODO
    #config.add_route('alpha', 'opds/alpha')
    #config.add_route('new', 'opds/new')
    #config.add_route('publisher', 'opds/publisher')
    config.scan()
    config.add_renderer('opds', factory='scieloopds.renderers.opds_factory')
    return config.make_wsgi_app()