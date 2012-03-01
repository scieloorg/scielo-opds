

class Link(object):
    __slots__ = ('_href', '_rel', '_type', '_title')

    def __init__(self, href, rel, type, title=None):
        args = locals().copy()
        del args['self']
        for name in args:
            setattr(self, '_'+name, args[name])

    def as_dict(self):
        return {k[1:]: getattr(self, k) for k in self.__slots__
                if getattr(self, k) is not None}
