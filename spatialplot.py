# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpatialPlot
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from spatialplotdialog import SpatialPlotDialog
import os.path


class SpatialPlot:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'spatialplot_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/spatialplot/icon.png"),
            u"Spatial Plot", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToVectorMenu(u"&Spatial Plot", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginVectorMenu(u"&Spatial Plot", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
    
        if (self.iface.mapCanvas().currentLayer() is None or
            not isinstance(self.iface.mapCanvas().currentLayer(), QgsVectorLayer)):
            self.iface.messageBar().pushMessage("Error", "You'll need to select a Vector layer first...", level=QgsMessageBar.CRITICAL)
            return
            
    
        # Create the dialog (after translation) and keep reference
        self.dlg = SpatialPlotDialog(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dlg)
        
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
        #    pass
