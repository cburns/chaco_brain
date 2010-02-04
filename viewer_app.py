
import logging

from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
from enthought.envisage.ui.workbench.api import WorkbenchApplication

from slice_view_plugin import SliceViewUIPlugin, SliceViewPlugin

# Logging
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(file('viewer_app.log', 'w')))
logger.setLevel(logging.DEBUG)

class ChacoViewer(WorkbenchApplication):
    id = 'nipy.viz'
    name = 'Chaco Brain'


def main():
    chaco_brain_app = ChacoViewer(
        plugins = [CorePlugin(), WorkbenchPlugin(), SliceViewPlugin(),
                   SliceViewUIPlugin(),
                   ]
        )

    chaco_brain_app.run()
    return

if __name__ == '__main__':
    main()
