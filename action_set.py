"""Action set for menus and actions."""

from enthought.envisage.ui.action.api import Action, ActionSet, Group, Menu

# Groups
file_group = Group(
    id = 'ChacoBrainFileGroup',
    path = 'MenuBar/File',
    before = 'ExitGroup'
    )

# Menus
open_menu = Menu(
    id = 'OpenFileMenu',
    name = '&Open file menu...',
    path = 'MenuBar/File',
    #group = 'ChacoBrainFileGroup'
    )

# Actions
open_file = Action(
    id = 'OpenFile',
    class_name = 'io.OpenFile',
    name = '&Open file ...',
    path = 'MenuBar/File',
    #before = 'ExitGroup'
    )

class ChacoBrainUIActionSet(ActionSet):
    #groups = [file_group]
    #menus = [open_menu]
    actions = [open_file]

