"""Nipy viewer using Enthought Tools."""

# In learning Envisage, I modeled much of this code off of the lorenz
# example: ETS_3.3.1/EnvisagePlugins_3.1.2/examples/workbench/Lorenz

import logging

from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin

from chaco_brain_app import ChacoBrainApplication

# Logging
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(file('chaco_brain.log', 'w')))
#logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def main():
    chaco_brain_app = ChacoBrainApplication(
        plugins = [CorePlugin(), WorkbenchPlugin()]
        )

    chaco_brain_app.run()
    return

if __name__ == '__main__':
    main()
