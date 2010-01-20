
from enthought.envisage.api import Plugin
from enthought.traits.api import List
from enthought.pyface.workbench.api import TraitsUIView
from enthought.pyface.workbench.api import Perspective, PerspectiveItem

class SliceViewPerspective(Perspective):
    name = 'SliceViewPerp' # Name that appears in the View > Perspectives menu
    show_editor_area = False
    contents = [
        PerspectiveItem(id='SliceView')
        ]

class SliceViewPlugin(Plugin):
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    VIEWS = 'enthought.envisage.ui.workbench.views'

    id = 'nipy.viz'
    name = 'Slice View Plugin'

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
