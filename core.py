"""The core object will hold the instance of the data so that other
plugins can easily access it."""

from enthought.traits.api import HasTraits, Instance

from image import Image

class Core(HasTraits):
    img = Instance(Image)
    # Need a way to notify that the image has changed!
