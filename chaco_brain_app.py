
from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import AboutDialog, ImageResource

class ChacoBrainApplication(WorkbenchApplication):
    """The Chaco Brain application."""

    id = 'nipy.viz.chaco_brain'
    name = 'Chaco Brain'

    def _about_dialog_default(self):
        """ Trait initializer. """

        about_dialog = AboutDialog(
            parent = self.workbench.active_window.control,
            image  = ImageResource('about')
        )

        return about_dialog
