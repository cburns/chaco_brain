
from enthought.envisage.api import Plugin, ServiceOffer
from enthought.traits.api import List
from enthought.pyface.workbench.api import TraitsUIView
from enthought.pyface.workbench.api import Perspective, PerspectiveItem


class SliceViewPerspective(Perspective):
    name = 'SliceViewPerp' # Name that appears in the View > Perspectives menu
    show_editor_area = False
    contents = [
        PerspectiveItem(id='SliceView')
        ]

class SliceViewUIPlugin(Plugin):
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    VIEWS = 'enthought.envisage.ui.workbench.views'
    ACTION_SETS = 'enthought.envisage.ui.workbench.action_sets'

    id = 'nipy.viz_ui'
    name = 'Slice View UI Plugin'

    perspectives = List(contributes_to=PERSPECTIVES)
    def _perspectives_default(self):
        return [SliceViewPerspective]

    views = List(contributes_to=VIEWS)
    def _views_default(self):
        return [self._create_slice_view]

    def _create_slice_view(self, **traits):
        from slice_view import Viewer
        viewer = Viewer()
        view = TraitsUIView(
            id = 'SliceView',
            name = '3D View', # Name that appears in the View menu and Tab
            obj = viewer,
            **traits
            )
        return view

    action_sets = List(contributes_to=ACTION_SETS)
    def _action_sets_default(self):
        from action_set import ChacoBrainUIActionSet
        return [ChacoBrainUIActionSet]


class SliceViewPlugin(Plugin):
    SERVICE_OFFERS = 'enthought.envisage.ui.workbench.service_offers'
    
    id = 'nipy.viz'
    name = 'Slice View Plugin'

    service_offers = List(contributes_to=SERVICE_OFFERS)
    def _service_offers_default(self):
        core_service_offer = ServiceOffer(
            protocol = 'core.Core',
            factory = 'core.Core'
            )

        services_service_offer = ServiceOffer(
            protocol = 'services.Services',
            factory = 'services.Services'
            )
        return [core_service_offer, services_service_offer]
