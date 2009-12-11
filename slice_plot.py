
from enthought.chaco.api import (ArrayPlotData, Plot, gray, GridContainer,
                                 OverlayPlotContainer, GridDataSource, 
                                 HPlotContainer)
from enthought.enable.component_editor import ComponentEditor
from enthought.traits.api import (HasTraits, Instance, DelegatesTo, 
                                  on_trait_change, Enum, Array, Int, Str,
                                  Color, List, Trait, Callable, Dict)
from enthought.traits.ui.api import (Item, View, Menu, MenuBar, Action,
                                     OKButton, CancelButton)
from enthought.chaco.tools.cursor_tool import CursorTool, BaseCursorTool
import enthought.chaco.default_colormaps as chaco_colormaps
from enthought.enable.api import BaseTool
from enthought.chaco.tools.api import LineInspector


# File IO imports
from enthought.traits.api import File, Button
from enthought.traits.ui.api import HGroup
from enthought.traits.ui.file_dialog import open_file

from image import Image

def load_image():
    file_name = File
    file_name = open_file()
    if file_name != '':
        img = Image(file_name)
        return img, file_name
    else:
        return None, None

class Crosshairs(BaseTool):
    event_state = Enum("normal", "mousedown")
    
    def map_data(self, event):
        # Map event coords to data coords.
        x = self.component.x_mapper.map_data(event.x)
        y = self.component.y_mapper.map_data(event.y)
        return x, y

    def normal_left_down(self, event):
        self.event_state = 'mousedown'
        #print 'normal_left_down:', event.x, event.y

        for olay in self.component.overlays:
            # Set initial position of the CursorTool if there is one.
            #print 'olay:', olay
            if hasattr(olay, 'current_position'):
                #print 'current_position!'
                x, y = self.map_data(event)
                olay.current_position = x, y
        event.handled = True

    def mousedown_mouse_move(self, event):
        # XXX this func unnecessary as the CursorTool sets position
        x, y = self.map_data(event)
        #print 'mousedown_mouse_move', x, y

    def mousedown_left_up(self, event):
        #print 'mousedown_left_up'
        self.event_state = "normal"
        event.handled = True

class Voxel(HasTraits):
    x = Int
    y = Int
    z = Int

    #@on_trait_change('x, y, z')
    #def _anytrait_changed(self, name, old, new):
        #print 'Voxel changed:', name, old, new
        #print self

    def __repr__(self):
        # Voxel(x, y, z)
        outstr = 'Voxel(%d, %d, %d)' % (self.x, self.y, self.z)
        return outstr

class SlicePlot(Plot):
    cursor = Instance(BaseCursorTool)
    cursor_pos = DelegatesTo('cursor', prefix='current_position')
    voxel = Instance(Voxel)
    xindex = Int
    yindex = Int

    def __init__(self, data, **kwtraits):
        super(SlicePlot, self).__init__(data, **kwtraits)
        self.voxel = kwtraits.get('voxel') # XXX what to set for default?

    def set_slice(self, name):
        self.renderer = self.img_plot(name, hide_grids=False, 
                                      colormap=chaco_colormaps.gray)[0]
        self.slicename = name
        self.init_cursor()

    def init_cursor(self):
        # Adding a cursor to the axial plot to test cursor
        # functionality in Chaco
        self.cursor = CursorTool(self.renderer, drag_button='left', 
                                 color='blue')
        x, y = self.data.get_data(self.slicename).shape
        self.cursor.current_position = x/2, y/2
        #self.cursor.current_position = self.voxel.x, self.voxel.y
        self.renderer.overlays.append(self.cursor)
        self.renderer.tools.append(Crosshairs(self.renderer))


    @on_trait_change('xindex, yindex')
    def _index_changed(self, name, old, new):
        # Event handler, triggered when mouse left down event happens
        # in plot.

        #print '_index_changed:', name, old, new
        #print self.slicename, '._index_changed'
        self.cursor.current_position = self.xindex, self.yindex

    def _cursor_pos_changed(self, name, old, new):
        self.xindex, self.yindex = self.cursor_pos
        #print self.slicename, '._cursor_pos_changed:', self.xindex, self.yindex
        #print 'cursor_pos (%d, %d)' % (x, y)
        #print 'voxel:', self.voxel.get('x', 'y', 'z')
        #print 'intensity:', self.data[y,x]

    def redraw(self):
        """Redraw the plot."""
        self.renderer.request_redraw()

    def set_colormap(self, cmap):
        """Set the colormap of the plot.

        Parameters
        ----------
        cmap : str or chaco callable colormap
            A colormap name or a colormap from
            enthought.chaco.default_colormaps

        """

        clr_range = self.renderer.color_mapper.range
        try:
            # Try chaco colormap
            color_mapper = cmap(clr_range)
        except TypeError:
            # If cmap is not callable (like if it's a string)
            try:
                # Try cmap as a string
                cmap = chaco_colormaps.color_map_name_dict[cmap]
                color_mapper = cmap(clr_range)
            except KeyError:
                # Not a string assume a chaco colormap function
                msg = "Unable to find colormap '%s'" % cmap
                raise KeyError(msg)
        self.renderer.color_mapper = color_mapper
        self.redraw()

#
# Menus and actions
#
file_open = Action(name = "Open...", action = "load_image")
menu_file = Menu(file_open, name = "File")
preferences = Action(name = "Preferences", action = "set_preferences")
menu_viewer = Menu(preferences, name = "Viewer")
menubar = MenuBar(menu_viewer, menu_file)

class Preferences(HasTraits):
    colormap = Enum(chaco_colormaps.color_map_name_dict.keys())
    cmap = Trait(chaco_colormaps.gray, Callable)

    traits_view = View(Item('colormap'),
                       title = "Preferences",
                       buttons = [OKButton, CancelButton],
                       resizable = True)

    def __init__(self):
        super(Preferences, self).__init__()

    def _colormap_changed(self):
        self.cmap = chaco_colormaps.color_map_name_dict[self.colormap]

def launch_prefs(caller):
    # XXX Need to think about better way to handle preferences.  Just
    # handling colormap for now.  Need to abstract preferences into an
    # object that can be serialized and easily passed between objects
    # (a dict?).  Also when we open the preferences, the value in the
    # drop-down list is just the first in the chaco_colormaps dict,
    # not the current colormap of the plots.  Again, a more robust
    # solution would fix this.
    prefs = Preferences()
    prefs.edit_traits(kind='modal')
    try:
        caller.update_preferences(prefs.cmap)
    except AttributeError:
        pass


class Viewer(HasTraits):
    plot = Instance(GridContainer)
    container = GridContainer(shape=(2,2))
    plotdata = Instance(ArrayPlotData)
    voxel = Instance(Voxel)
    img = Instance(Image)

    traits_view = View(
            Item('plot', editor=ComponentEditor(), show_label=False), 
            width=800, height=600,
            resizable=True,
            title = "Image Plot",
            menubar = menubar)

    def __init__(self):
        super(Viewer, self).__init__()
        
        self.load_image()

        axl_plt = SlicePlot(self.plotdata, voxel=self.voxel)
        axl_plt.set_slice('axial')
        axl_plt.sync_trait('xindex', self.voxel, alias='x')
        axl_plt.sync_trait('yindex', self.voxel, alias='y')

        cor_plt = SlicePlot(self.plotdata, voxel=self.voxel)
        cor_plt.set_slice('coronal')
        cor_plt.sync_trait('xindex', self.voxel, alias='x')
        cor_plt.sync_trait('yindex', self.voxel, alias='z')

        sag_plt = SlicePlot(self.plotdata, voxel=self.voxel)
        sag_plt.set_slice('sagittal')
        sag_plt.sync_trait('xindex', self.voxel, alias='y')
        sag_plt.sync_trait('yindex', self.voxel, alias='z')

        # Add our plots to the GridContainer
        self.container.add(axl_plt)
        self.container.add(cor_plt)
        self.container.add(sag_plt)

        self.plot = self.container

    def update_slices(self):
        # Update image slices based on selecte voxel coords.
        axial = self.img.get_axial_slice(self.voxel.z)
        coronal = self.img.get_coronal_slice(self.voxel.y)
        sagittal = self.img.get_sagittal_slice(self.voxel.x)

        if self.plotdata is None:
            # Create array data container
            self.plotdata = ArrayPlotData(axial=axial, 
                                          sagittal=sagittal, 
                                          coronal=coronal)
        else:
            self.plotdata.set_data('axial', axial)
            self.plotdata.set_data('coronal', coronal)
            self.plotdata.set_data('sagittal', sagittal)

    @on_trait_change('voxel.[x,y,z]')
    def _voxel_changed(self, name, old, new):
        #print '_voxel_changed, name:', name, 'old:', old, 'new:', new
        self.update_slices()

    def load_image(self, info=None):
        # Load image
        img, filename = load_image()
        if img is not None:
            self.img = img
            self.filename = filename
            xdim, ydim, zdim = self.img.shape
            if self.voxel is None:
                self.voxel = Voxel(x=xdim/2, y=ydim/2, z=zdim/2)
            else:
                self.voxel.x = xdim/2
                self.voxel.y = ydim/2
                self.voxel.z = zdim/2
            self.update_slices()

    def set_preferences(self, info=None):
        # XXX Separate Handler from view and attach actions to the
        # handler.  This might allow me to have the preferenceces be
        # separate View from the plot viewer. ???
        launch_prefs(self)

    def update_preferences(self, cmap):
        for plot in self.container.components:
            plot.set_colormap(cmap)

if __name__ == '__main__':
    viewer = Viewer()
    viewer.configure_traits()
