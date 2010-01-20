"""The plugin component for plot_params."""

from enthought.envisage.api import Plugin, ServiceOffer
from enthought.traits.api import List, on_trait_change

class MovementParamPlugin(Plugin):
    """The Movement Parameter Plugin.

    Plugin to handle interfaces with the MovementParamPlot class.
    """

    # plugin's unique id
    id = 'nipy.viz.movement_params'
    name = 'Movement Parameters'

    # Little unclear on the whole ServiceOffer things. Need to search
    # for more documentation.
    service_offers = List(contributes_to='enthought.envisage.service_offers')
    
    def _service_offers_default(self):
        movement_params_service_offer = ServiceOffer(
            protocol = 'plot_params.MovementParamPlot',
            #factory = 'plot_params.MovementParamPlot',
            factory = self._create_movement_params_service
            )
        return [movement_params_service_offer]

    def _create_movement_params_service(self):
        from plot_params import MovementParamPlot
        return MovementParamPlot()

    @on_trait_change('application:started')
    def _plot_movement_params(self):
        from plot_params import MovementParamPlot
        plt_prms = self.application.get_service(MovementParamPlot)
        return
