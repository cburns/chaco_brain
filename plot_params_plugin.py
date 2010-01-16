"""The plugin component for plot_params."""

from enthought.envisage.api import Plugin, ServiceOffer
from enthought.traits.api import List

class MovementParamPlugin(Plugin):
    """The Movement Parameter Plugin.

    Plugin to handle interfaces with the MovementParamPlot class.
    """

    # plugin's unique id
    id = 'nipy.viz.movement_params'
    name = 'Movement Parameters'

    # Little unclear on the whole ServiceOffer things. Need to search
    # for more documentation.
    service_offers = List(contributes_to='nipy.viz.service_offers')
    
    def _service_offers_default(self):
        movement_params_service_offer = ServiceOffer(
            protocol = 'plot_params.MovementParamPlot',
            factory = 'plot_params.MovementParamPlot',
            )
        return [movement_params_service_offer]


