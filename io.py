"""Module to handle io actions.  Mostly thinking of this in terms of
the MenuBar, items like the File>Open menu.  """

import os

from enthought.traits.api import Str
from enthought.pyface.api import FileDialog, OK
from enthought.pyface.action.api import Action

#from enthought.traits.api import File
#from enthought.traits.ui.file_dialog import open_file

from services import get_ichaco_brain, get_core

class OpenFile(Action):
    """Open a data file."""
    tooltip = "Open a data file"
    description = tooltip
    path = Str("MenuBar/File")

    def perform(self, event):
        # Get services offered by chaco_brain
        svc = get_ichaco_brain(self.window)
        core = get_core(self.window)
        wildcard = 'All files (*.*)|*.*'

        parent = self.window.control
        dialog = FileDialog(parent=parent,
                            title='Open data file',
                            action='open', wildcard=wildcard
                            )
        if dialog.open() == OK:
            if not os.path.isfile(dialog.path):
                # XXX Need to handle errors!
                #error("File '%s' does not exist!"%dialog.path, parent)
                print "Unable to open file '%s'!" % dialog.path
                return
            img = svc.open(dialog.path)
            core.img = img

# from image import Image

# def load_image():
#     """Handler for File > Open menu"""
#     file_name = File
#     file_name = open_file()
#     if file_name != '':
#         img = Image(file_name)
#         return img, file_name
#     else:
#         return None, None

# if __name__ == '__main__':
#     img, file_name = load_image()
#     print file_name

