"""A module to hold access to the services offered to the plugins.

XXX Need better name.
"""

from enthought.traits.api import HasTraits

def get_ichaco_brain(window):
    """Return the ICHACO_BRAIN service.

    Given an Envisage workbench window.
    """
    # return window.get_service(Services)
    svc = window.get_service(Services)
    print 'get_ichaco_brain svc:', svc
    return svc

def get_core(window):
    from core import Core
    #return window.get_service(Core)
    svc = window.get_service(Core)
    print 'get_core svc:', svc
    return svc

class Services(HasTraits):
    def open(self, filename):
        from image import Image
        return Image(filename)
