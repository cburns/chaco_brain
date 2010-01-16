from enthought.envisage.api import Plugin
from enthought.pyface.workbench.api import Perspective, PerspectiveItem
from enthought.pyface.workbench.api import TraitsUIView
from enthought.traits.api import List

class MovementParamsPerspective(Perspective):
    """A perspective containing the rotation and translation movement params.

    """
    
    name = 'Movement Parameters'
    show_editor_area = False # XXX what's this?

    contents = [
        PerspectiveItem(id='movement_params.plot'),
        ]
    
class MovementParamUIPlugin(Plugin):
    """The Movement Parameter UI Plugin

    Provides interface to the plot_param TraitUIs for the chaco_brain app.

    """

    # Extension point IDs
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    VIEWS = 'enthought.envisage.ui.workbench.views'

    # XXX FIgure out convention for these.
    id = 'nipy.viz.movement_param_ui'

    name = 'Movement Parameters UI'

    # This plugin's contributions to various extension points
    perspectives = List(contributes_to=PERSPECTIVES)
    def _perspectives_default(self):
        return [MovementParamsPerspective]

    views = List(contributes_to=VIEWS)
    def _view_default(self):
        return [self._create_movement_params_plot]

    def _create_movement_params_plot(self, **traits):
        """Factory method to create the movement parameters plot."""

        from plot_params import MovementParamPlot

        # XXX Begin hack to just to get the GUI working
#         import numpy as np
#         from plot_params import PARAM_DTYPE

#         fnames = ['data/movement_params.txt']
#         params = np.recfromtxt(fname, dtype=PARAM_DTYPE)
        # XXX End hack
        
        data_view = TraitsUIView(
            id = 'movement_params.plot',
            name = 'Movement Parameters',
            #obj = MovementParamPlot(fnames, params),
            obj = MovementParamsView(movement_params = \
                      self.application.get_service(MovementParamPlot)),
            **traits
            )

        return data_view
