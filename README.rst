=============
 Chaco Brain
=============

The goal of chaco-brain is to create an interactive viewer for 3D and
4D image volumes.  Ideally we will borrow the best ideas from other
imaging viewers and take advantage of the strengths of Traits and
Chaco.

Usage::

  python slice_plot.py

Problems
--------

- Currently there is hard coding such that the code only works with 3D
  volumes.  This needs to be abstracted so we can support 4D volumes
  and view voxel time-series when voxels are selected.

- Have to select a file when the application opens, shouldn't require
  the user to do this.  Should have a dummy or blank plots until uses
  chooses File > Open.

- image.py is a hack.  This is a placeholder until we can use the Nipy
  Image class or brifti for getting this info.

- Need storage for user preferences.  Currently the user can select
  the colormap for the images, but when they reopen the Preferences
  the "top" cmap is selected, not the currently active cmap because we
  don't save this info.




