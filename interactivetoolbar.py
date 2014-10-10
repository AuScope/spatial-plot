# -*- coding: utf-8 -*-
"""
/***************************************************************************
 InteractiveToolbar

 A matplotlib toolbar customised for more interactivity
                             -------------------
        begin                : 2014-09-02
        copyright            : (C) 2014 by Josh Vote (CSIRO)
        email                : Josh.Vote@csiro.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSignal
import matplotlib
import os
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg

import statist_utils as utils

class InteractiveToolbar(NavigationToolbar2QTAgg):

    """ Raised whenever a successful selection is made. Return type is data range in the x axis"""
    select_plot = pyqtSignal(float, float, name='select_plot')

    def __init__(self, plotCanvas, dialog):
        NavigationToolbar2QTAgg.__init__(self, plotCanvas, dialog)
        
        self._select_mode_events = []
    
    def _init_toolbar(self):
        selectAction = self.addAction(QIcon(":/plugins/spatialplot/action.png"), 'Select Features', self.select_mode)
        selectAction.setToolTip('Click and drag the plot to select features in the QGIS interface.')
        selectAction.setCheckable(True)
        self._actions['select'] = selectAction
        
        NavigationToolbar2QTAgg._init_toolbar(self)
    
    """ Call to update the "checked" status of the toolbar buttons"""
    def _update_buttons_checked(self):
        NavigationToolbar2QTAgg._update_buttons_checked(self)
        self._actions['select'].setChecked(self._active == 'SELECT')
    
    """ Enable selection of features by dragging on the plot """
    def select_mode(self):
        if self._active == 'SELECT':
            self._active = None
        else:
            self._active = 'SELECT'
            
        if self._active:
            self._select_mode_events.append(self.canvas.mpl_connect('button_press_event',
                                                    self.select_mode_mouse_down))
            self._select_mode_events.append(self.canvas.mpl_connect('button_release_event',
                                                      self.select_mode_mouse_up))
            self.mode = 'Drag a selection box'
            self.canvas.widgetlock(self)
        else:
            self.mode = ''
            self.select_mode_deregister_events()
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)

        self.set_message(self.mode)    
        
        self._update_buttons_checked()
    
    def select_mode_deregister_events(self):
        for select_id in self._select_mode_events:
            self.canvas.mpl_disconnect(select_id)
        self._select_mode_events = []
    
    """ Handle mouse dragging when select mode is active"""
    def select_mode_drag(self, event):
        if self._xypress:
            x, y = event.x, event.y
            lastx, lasty, a, ind, lim, trans = self._xypress[0]

            # adjust x, last, y, last
            x1, y1, x2, y2 = a.bbox.extents
            x, lastx = max(min(x, lastx), x1), min(max(x, lastx), x2)
            y, lasty = max(min(y, lasty), y1), min(max(y, lasty), y2)

            self.draw_rubberband(event, x, y, lastx, lasty)
    
    def select_mode_mouse_up(self, event):
        self.select_mode_deregister_events()

        if not self._xypress:
            return

        last_a = []

        for cur_xypress in self._xypress:
            x, y = event.x, event.y
            lastx, lasty, a, ind, lim, trans = cur_xypress
            # ignore singular clicks - 5 pixels is a threshold
            if abs(x - lastx) < 5 or abs(y - lasty) < 5:
                self._xypress = None
                self.release(event)
                self.draw()
                return

            x0, y0, x1, y1 = lim.extents

            # zoom to rect
            inverse = a.transData.inverted()
            lastx, lasty = inverse.transform_point((lastx, lasty))
            x, y = inverse.transform_point((x, y))
            Xmin, Xmax = a.get_xlim()
            Ymin, Ymax = a.get_ylim()

            # detect twinx,y axes and avoid double zooming
            twinx, twiny = False, False
            if last_a:
                for la in last_a:
                    if a.get_shared_x_axes().joined(a, la):
                        twinx = True
                    if a.get_shared_y_axes().joined(a, la):
                        twiny = True
            last_a.append(a)

            if twinx:
                x0, x1 = Xmin, Xmax
            else:
                if Xmin < Xmax:
                    if x < lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 < Xmin:
                        x0 = Xmin
                    if x1 > Xmax:
                        x1 = Xmax
                else:
                    if x > lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 > Xmin:
                        x0 = Xmin
                    if x1 < Xmax:
                        x1 = Xmax

            if twiny:
                y0, y1 = Ymin, Ymax
            else:
                if Ymin < Ymax:
                    if y < lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 < Ymin:
                        y0 = Ymin
                    if y1 > Ymax:
                        y1 = Ymax
                else:
                    if y > lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 > Ymin:
                        y0 = Ymin
                    if y1 < Ymax:
                        y1 = Ymax
                        
            self.select_plot.emit(x0, x1)

        self.draw()
        self._xypress = None
        self._button_pressed = None

        self.push_current()
        self.release(event)
        
        self.select_mode() #Turn off select mode
        
    def select_mode_mouse_down(self, event):    
        if event.button == 1:
            self._button_pressed = 1
        elif event.button == 3:
            self._button_pressed = 3
        else:
            self._button_pressed = None
            return

        x, y = event.x, event.y
        
        self._xypress = []
        for i, a in enumerate(self.canvas.figure.get_axes()):
            if (x is not None and y is not None and a.in_axes(event) and
                    a.get_navigate() and a.can_zoom()):
                self._xypress.append((x, y, a, i, a.viewLim.frozen(),
                                      a.transData.frozen()))

        self._select_mode_events.append(self.canvas.mpl_connect('motion_notify_event', self.select_mode_drag))

        self.press(event)
