#!/usr/bin/env python

# Standard libs
import re
from warnings import warn, simplefilter


# Third party libs
import argparse

import numpy as np
from enthought.enable.api import ComponentEditor
import enthought.traits.api as traits
import enthought.traits.ui.api as ui
import enthought.chaco.api as chaco
import enthought.chaco.tools.api as tools

PARAM_DTYPE = [('rot', [('x', 'f4'), ('y', 'f4'), ('z', 'f4')]), 
               ('trans', [('x', 'f4'), ('y', 'f4'), ('z', 'f4')])]

# cmap = chaco.Spectral(chaco.DataRange1D(low=0, high=5))
# COLOR_PALETTE = cmap.color_bands

    
class MovementParamPlot(traits.HasTraits):
    # "Internal" attributes
    data = traits.DictStrAny(value_trait=chaco.ArrayPlotData)
    zoom = traits.Instance(tools.ZoomTool)
    pan = traits.Instance(tools.PanTool)
    # Would be nice to actually make this a list of files - but maybe not here,
    # as we may want to load the file-names from a canned report datasource
    # (i.e. the original files may not be present)
    file_list = traits.List(trait=traits.Str)
    
    # Attributes in the view
    rot_plot = traits.Instance(chaco.Plot)
    trans_plot = traits.Instance(chaco.Plot)
    # It'd be nice to split out the notion of which subject is selected, so that
    # this plot can simply take a given set of data
    max_params = traits.Int(0)
    params_num = traits.Range(0, 'max_params') 
    file_name = traits.Str('file_name not set')

    print '*'*80
    print 'MovementParamPlot class'
    1/0

    """
    traits_view = ui.View( 
                    ui.Item('params_num', label="Scan Number",
                            editor=ui.RangeEditor(mode='spinner',
                                                  high_name='max_params') ),
                    ui.Item('file_name', label='File', style='readonly'),
                    ui.Item('rot_plot', label='Rotation', 
                            editor=ComponentEditor(height=300)),
                    ui.Item('trans_plot', label='Translation', 
                            editor=ComponentEditor(height=300)),
                    # width=550, 
                    # height=750, 
                    resizable=True, 
                    title="Movement parameters"
                  )
                  """

    def __init__(self, fnames=None, params=None):
        '''params: a list of numpy arrays'''
        super(MovementParamPlot, self).__init__()

        if fnames is None:
            # XXX Hardcode hack to get envisage working
            fnames = ['data/movement_params.txt']
            params = np.recfromtxt(fnames[0], dtype=PARAM_DTYPE)

        self.file_list = fnames
        self.file_name = fnames[0]
        self.params_num = 0
        self.max_params = len(params) - 1

        self.params = params

        print '*'*80
        print 'plot_params, file_name:', self.file_name
        1/0

        # XXX - the following info should go (soon) into 
        # nipype.interfaces.fsl.McFLIRT
        self.trans_plot = self.create_line_plot('trans', 'mm')
        self.rot_plot = self.create_line_plot('rot', 'radians (clockwise)',
                                              self.trans_plot.index_range)

        # Note - it doesn't matter which plot you use to init the tools
        self.zoom = tools.ZoomTool(self.trans_plot, tool_mode='range', 
                                   axis='index')
        self.pan = tools.PanTool(self.rot_plot, constrain=True,
                                 constrain_direction='x')
        self.trans_plot.tools.extend((self.zoom, self.pan))
        self.rot_plot.tools.extend((self.pan, self.zoom))


    def create_line_plot(self, name, units='Arbitrary Units', 
                         index_range=None):
        '''Make a line plot overlaying x, y and z values'''
        data = chaco.ArrayPlotData()
        plot = chaco.Plot(data)
        if index_range is not None:
            plot.index_range = index_range

        xyz = self.params[0][name]
        axes = xyz.dtype.names
        for axis in axes:
            data.set_data(axis, xyz[axis])
            plot.plot(axis, color='auto')

        plot.index_axis.title = 'Slice Number'
        plot.value_axis.title = units
        # Our left axis labels are a bit large
        plot.padding = [70, 50, 20, 50]
        # might be clearer to write:
        # plot.padding_top = 20
        # plot.padding_left = 70

        plot.legend.tools.append(
                tools.LegendTool(plot.legend, drag_button="right") )
        plot.legend.labels = list(axes)
        plot.legend.visible = True

        self.data[name] = data

        return plot

    # TODO: need to re-set range on plots
    @traits.on_trait_change('params_num')
    def set_plot(self, n=None):
        if n is None:
            n = self.params_num
        else:
            self.params_num = n
        
        self.file_name = self.file_list[n]

        params = self.params[n]
        for name in params.dtype.names:
            xyz = params[name]
            for axis in xyz.dtype.names:
                self.data[name].set_data(axis, xyz[axis])

# XXX Not sure if this is the best way to split the view out but doing
# this to try and get the envisage framework working.  Modelling the
# code after the EnvisagePlugins Lorenz example.
class MovementParamsView(traits.HasTraits):
    movement_params = traits.Instance(MovementParamPlot)

    params_num = traits.DelegatesTo('movement_params')
    max_params = traits.DelegatesTo('movement_params')
    file_name = traits.DelegatesTo('movement_params')
    rot_plot = traits.DelegatesTo('movement_params')
    trans_plot = traits.DelegatesTo('movement_params')

    traits_view = ui.View( 
                    ui.Item('params_num', label="Scan Number",
                            editor=ui.RangeEditor(mode='spinner',
                                                  high_name='max_params') ),
                    ui.Item('file_name', label='File', style='readonly'),
                    ui.Item('rot_plot', label='Rotation', 
                            editor=ComponentEditor(height=300)),
                    ui.Item('trans_plot', label='Translation', 
                            editor=ComponentEditor(height=300)),
                    # width=550, 
                    # height=750, 
                    resizable=True, 
                    title="Movement parameters"
                  )

class TimediffPlot(traits.HasTraits):
    traits_view = ui.View( 
                    ui.Item('params_num', label="Scan Number",
                            editor=ui.RangeEditor(mode='spinner',
                                                  high_name='max_params') ),
                    ui.Item('rot_plot', label='Rotation', 
                            editor=ComponentEditor()),
                    ui.Item('trans_plot', label='Translation', 
                            editor=ComponentEditor()),
                    # width=550, height=550, 
                    resizable=True, 
                    title="Movement parameters"
                  )
       
class PhysioPlot(traits.HasTraits):
    traits_view = ui.View( 
                    ui.Item('params_num', label="Scan Number",
                            editor=ui.RangeEditor(mode='spinner',
                                                  high_name='max_params') ),
                    ui.Item('rot_plot', label='Rotation', 
                            editor=ComponentEditor()),
                    ui.Item('trans_plot', label='Translation', 
                            editor=ComponentEditor()),
                    # width=550, height=550, 
                    resizable=True, 
                    title="Movement parameters"
                  )
def main(fnames, verbose=False, plot=True):
    '''main(fnames): simply reads each file in fnames'''
    if verbose:
        simplefilter('always', UserWarning)
    else:
        simplefilter('ignore', UserWarning)

    # Allow passing in a single string
    if isinstance(fnames, str):
        fnames = [fnames]

    params = []
    for fname in fnames:
        params.append(np.recfromtxt(fname, dtype=PARAM_DTYPE))

    plot_obj = MovementParamPlot(fnames, params)
    plot_obj.configure_traits()
    return plot_obj

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true') 
    parser.add_argument('fnames', nargs='+')
    args = parser.parse_args()
    main(args.fnames, verbose=args.verbose, plot=False)
