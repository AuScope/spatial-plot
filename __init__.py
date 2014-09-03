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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load SpatialPlot class from file SpatialPlot
    from spatialplot import SpatialPlot
    return SpatialPlot(iface)
