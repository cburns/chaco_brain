"""Interface to nipy image."""

from nipype.externals import pynifti

class Image(object):
    def __init__(self, filename=None):
        self.img = None
        self.filename = filename
        if filename is not None:
            self.load_image(filename)

    def load_image(self, filename):
        img = pynifti.load(filename)
        self.img = img
        self.filename = filename
        self.data = self.img.get_data()

    def get_axial_slice(self, zindex):
        # XXX implement real slicing.  Assuming xyz ordering.
        data = self.data[:, :, zindex]
        # transpose so it's C ordered
        return data.T

    def get_coronal_slice(self, yindex):
        # XXX implement real slicing.  Assuming xyz ordering.
        data = self.data[:, yindex, :]
        # transpose so it's C ordered
        return data.T

    def get_sagittal_slice(self, xindex):
        # XXX implement real slicing.  Assuming xyz ordering.
        data = self.data[xindex, :, :]
        # transpose so it's C ordered
        return data.T

    @property
    def shape(self):
        return self.img.get_shape()

    @property
    def affine(self):
        return self.img.get_affine()


