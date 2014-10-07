# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpatialPlotDialog
                                 A QGIS plugin
 A plugin for plotting one or more attributes from a set of vector features
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from ui_spatialplot import Ui_SpatialPlot

import statist_utils as utils

import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from interactivetoolbar import InteractiveToolbar as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams

class SpatialPlotDialog(QDockWidget, Ui_SpatialPlot):

    CENTROID_X_FIELD = 'SP_GEOM_X'
    CENTROID_Y_FIELD = 'SP_GEOM_Y'
    FEATURE_ID_FIELD = 'SP_ID_FIELD'

    xAxis = None # The name (string) of the xAxis at the time of "plotting"
    axesPlotted=False # True if the user has hit the "Plot" button
    iface = None 
    highlight = None # A QgsVertexMarker (or None) representing a highlight placed on the map
    currentLayer = None # The QgsVectorLayer that will be used to generate plots
    
    def __init__(self, iface):
        QDockWidget.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        
        # Populate controls
        self.currentLayer = self.iface.mapCanvas().currentLayer()
        fieldNames = utils.getFieldNames(self.currentLayer, [QVariant.Int, QVariant.Double])
        self.pushButtonAdd.clicked.connect(self.addSelectedAttribute)
        self.pushButtonRemove.clicked.connect(self.removeSelectedAttribute)
        self.listWidgetAttributes.addItems(fieldNames)
        self.comboBoxXAxis.addItems(fieldNames)

        # Register for events
        self.currentLayer.selectionChanged.connect(self.onSelectionChanged)
        self.comboBoxXAxis.currentIndexChanged.connect(self.onXAxisChanged)

        #Plot lib
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.mpltoolbar = NavigationToolbar(self.canvas, self)
        lstActions = self.mpltoolbar.actions()
        self.mpltoolbar.removeAction(lstActions[7])
        self.mpltoolbar.select_plot.connect(self.onPlotSelect)
        self.verticalLayoutPlot.addWidget(self.canvas)
        self.verticalLayoutPlot.addWidget(self.mpltoolbar)
        self.canvas.mpl_connect('motion_notify_event', self.onMouseMove)
    
    def onXAxisChanged(self, newXAxis):
        self.plot()
    
    def onSelectionChanged(self, selected, deselected, clearAndSelect):
        self.plot()
    
    """ Raised whenever user drags and selects a portion of the map """
    def onPlotSelect(self, x0, x1):
        r = QgsFeatureRequest()
        r.setFilterExpression('{0} >= {1} AND {0} <= {2}'.format(self.xAxis, x0, x1))
        features = self.currentLayer.getFeatures(r)
        self.currentLayer.setSelectedFeatures([f.id() for f in features])
    
    """ Raised when the window is closing - use it to clean up """
    def closeEvent(self, evnt):
        self.removeHighlight()
        self.currentLayer.selectionChanged.disconnect(self.onSelectionChanged)
        self.comboBoxXAxis.currentIndexChanged.disconnect(self.onXAxisChanged)
    
    """ Removes the current feature highlight. No effect if the marker DNE """
    def removeHighlight(self):
        if self.highlight is not None:
            self.iface.mapCanvas().scene().removeItem(self.highlight)
        self.highlight = None
    
    """ Raised whenever the mouse moves over the plot """
    def onMouseMove(self, event):    
        self.removeHighlight()
        if not self.axesPlotted or not event.inaxes:
            return
        
        #Lookup xdata closest to mouseover location
        xAxisData = self.featureData[self.xAxis]
        x=event.xdata        
        closestIndex = np.searchsorted(xAxisData, event.xdata, side='left')
        if closestIndex == 0 or closestIndex >= len(xAxisData):
            return
        
        x = self.featureData[self.CENTROID_X_FIELD][closestIndex]
        y = self.featureData[self.CENTROID_Y_FIELD][closestIndex]
        self.highlight = QgsVertexMarker(self.iface.mapCanvas())
        self.highlight.setCenter(QgsPoint(x,y))
        self.highlight.setColor(QColor(255,0,0))
        self.highlight.setIconSize(30)
        self.highlight.setIconType(QgsVertexMarker.ICON_X)
        self.highlight.setPenWidth(3)
    
    def addSelectedAttribute(self):
        items = self.listWidgetAttributes.selectedItems()
        for item in items:
            rowToRemove = self.listWidgetAttributes.row(item)
            item = self.listWidgetAttributes.takeItem(rowToRemove)
            self.listWidgetYAxis.addItem(item)
        self.plot()
    
    def removeSelectedAttribute(self):
        items = self.listWidgetYAxis.selectedItems()
        for item in items:
            rowToRemove = self.listWidgetYAxis.row(item)
            item = self.listWidgetYAxis.takeItem(rowToRemove)
            self.listWidgetAttributes.addItem(item)
        self.plot()

    def getListWidgetValues(self, lw):
        values = []
        for i in range(0, lw.count()):
            values.append(lw.item(i).text())
        return values
        
    def clearPlot(self):
        self.axesPlotted = False
        self.xAxis = None
        self.featureData = None
        self.axes.clear()
        self.canvas.draw()
    
    def plot(self):
        if (self.comboBoxXAxis.currentText() is None or self.comboBoxXAxis.currentText() == ""):
            self.clearPlot()
            return
        
        if (self.listWidgetYAxis.count() == 0):
            self.clearPlot()
            return
        
        features = self.currentLayer.selectedFeatures()
        if (len(features) == 0):
            self.clearPlot()
            return
        
        self.xAxis = self.comboBoxXAxis.currentText()
        attributes = self.getListWidgetValues(self.listWidgetYAxis)
        attributes.append(self.xAxis)
        attributes = list(set(attributes)) # Get rid of duplicate values
        
        #Turn features into a numpy record array keyed by attributes
        dataTypes = [(str(x), np.float) for x in attributes]
        dataTypes.append((self.CENTROID_X_FIELD, np.float)) # We also cache the x/y for the mouseover highlight location
        dataTypes.append((self.CENTROID_Y_FIELD, np.float)) # We also cache the x/y for the mouseover highlight location
        self.featureData = np.recarray(len(features), dtype=np.dtype(dataTypes))
        idx = 0
        for feature in features:
            attributeValues = []
            for attribute in attributes:
                fieldIndex = feature.fields().indexFromName(attribute)
                attributeValues.append(feature.attributes()[fieldIndex])
                
            (x,y) = feature.geometry().centroid().asPoint()
            attributeValues.append(x)
            attributeValues.append(y)
            self.featureData[idx] = tuple(attributeValues)
            idx = idx + 1
    
        # Sort by x Axis
        self.featureData.sort(order=[str(self.xAxis)])
        
        
        # Make the plot
        xAxisData = self.featureData[self.xAxis]
        self.axes.clear()
        self.axes.set_title(self.tr(str(self.currentLayer.name())))
        
        lines = []
        for yAxis in self.getListWidgetValues(self.listWidgetYAxis):
            line = self.axes.plot(xAxisData, self.featureData[yAxis], label=str(yAxis))
            lines.append(line)   
        
        self.axes.legend()
        self.axes.set_xlabel(str(self.xAxis))
        self.figure.autofmt_xdate()
        self.canvas.draw()
        self.axesPlotted=True