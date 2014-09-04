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

from ui_spatialplot import Ui_SpatialPlot

import statist_utils as utils

import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams

class SpatialPlotDialog(QDialog, Ui_SpatialPlot):
    def __init__(self, iface):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        
        layer = self.iface.mapCanvas().currentLayer()
        fieldNames = utils.getFieldNames(layer, [QVariant.Int, QVariant.Double])
        
        self.pushButtonAdd.clicked.connect(self.addSelectedAttribute)
        self.pushButtonRemove.clicked.connect(self.removeSelectedAttribute)
        self.pushButtonPlot.clicked.connect(self.plot)
        
        self.listWidgetAttributes.addItems(fieldNames)
        self.comboBoxXAxis.addItems(fieldNames)
        
        #Plot lib
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.mpltoolbar = NavigationToolbar(self.canvas, self)
        lstActions = self.mpltoolbar.actions()
        self.mpltoolbar.removeAction(lstActions[7])
        self.verticalLayoutPlot.addWidget(self.canvas)
        self.verticalLayoutPlot.addWidget(self.mpltoolbar)
    
    def addSelectedAttribute(self):
        items = self.listWidgetAttributes.selectedItems()
        for item in items:
            rowToRemove = self.listWidgetAttributes.row(item)
            item = self.listWidgetAttributes.takeItem(rowToRemove)
            self.listWidgetYAxis.addItem(item)
    
    def removeSelectedAttribute(self):
        items = self.listWidgetYAxis.selectedItems()
        for item in items:
            rowToRemove = self.listWidgetYAxis.row(item)
            item = self.listWidgetYAxis.takeItem(rowToRemove)
            self.listWidgetAttributes.addItem(item)

    def getListWidgetValues(self, lw):
        values = []
        for i in range(0, lw.count()):
            values.append(lw.item(i).text())
        return values
        
    def plot(self):
        features = self.iface.mapCanvas().currentLayer().selectedFeatures()
        attributes = self.getListWidgetValues(self.listWidgetYAxis)
        attributes.append(self.comboBoxXAxis.currentText())
        attributes = list(set(attributes)) # Get rid of duplicate values
        
        #Turn features into a numpy record array keyed by attributes
        featureData = np.recarray(len(features), dtype=np.dtype([(str(x), np.float) for x in attributes]))
        idx = 0
        for feature in features:
            attributeValues = []
            for attribute in attributes:
                fieldIndex = feature.fields().indexFromName(attribute)
                attributeValues.append(feature.attributes()[fieldIndex])
            featureData[idx] = tuple(attributeValues)
            idx = idx + 1
    
        # Sort by sort field
        sortAttribute = self.comboBoxXAxis.currentText()
        featureData.sort(order=[str(sortAttribute)])
        
        
        # Make the plot
        xAxisData = featureData[self.comboBoxXAxis.currentText()]
        self.axes.clear()
        self.axes.set_title(self.tr(str(self.iface.mapCanvas().currentLayer().name())))
        
        lines = []
        for yAxis in self.getListWidgetValues(self.listWidgetYAxis):
            line = self.axes.plot(xAxisData, featureData[yAxis], label=str(yAxis))
            lines.append(line)   
        
        self.axes.legend()
        self.axes.set_xlabel(str(self.comboBoxXAxis.currentText()))
        self.figure.autofmt_xdate()
        self.canvas.draw()
        
    def logMessage(self, message):
        if globals().has_key('QgsMessageLog'):
            QgsMessageLog.logMessage(message, "SpatialPlot")