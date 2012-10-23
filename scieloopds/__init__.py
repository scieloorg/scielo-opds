from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/opds/')
    config.add_route('new', '/opds/new')
    config.add_route('alpha_catalog', '/opds/alpha')
    config.add_route('alpha_filter', '/opds/alpha/{id}')
    config.add_route('publisher_catalog', '/opds/publisher')
    config.add_route('publisher_filter', '/opds/publisher/{id}')
    config.scan()
    config.add_renderer('opds', factory='scieloopds.renderers.opds_factory')
    return config.make_wsgi_app()
