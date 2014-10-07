# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_spatialplot.ui'
#
# Created: Tue Oct 07 14:52:08 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SpatialPlot(object):
    def setupUi(self, SpatialPlot):
        SpatialPlot.setObjectName(_fromUtf8("SpatialPlot"))
        SpatialPlot.resize(594, 437)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.listWidgetAttributes = QtGui.QListWidget(self.dockWidgetContents)
        self.listWidgetAttributes.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetAttributes.setObjectName(_fromUtf8("listWidgetAttributes"))
        self.gridLayout.addWidget(self.listWidgetAttributes, 1, 0, 2, 2)
        self.pushButtonAdd = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonAdd.setSizePolicy(sizePolicy)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.gridLayout.addWidget(self.pushButtonAdd, 1, 2, 1, 1)
        self.listWidgetYAxis = QtGui.QListWidget(self.dockWidgetContents)
        self.listWidgetYAxis.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetYAxis.setObjectName(_fromUtf8("listWidgetYAxis"))
        self.gridLayout.addWidget(self.listWidgetYAxis, 1, 3, 2, 1)
        self.pushButtonRemove = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRemove.sizePolicy().hasHeightForWidth())
        self.pushButtonRemove.setSizePolicy(sizePolicy)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.gridLayout.addWidget(self.pushButtonRemove, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.comboBoxXAxis = QtGui.QComboBox(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.comboBoxXAxis.setFont(font)
        self.comboBoxXAxis.setObjectName(_fromUtf8("comboBoxXAxis"))
        self.gridLayout.addWidget(self.comboBoxXAxis, 3, 1, 1, 1)
        self.verticalLayoutPlot = QtGui.QVBoxLayout()
        self.verticalLayoutPlot.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayoutPlot.setObjectName(_fromUtf8("verticalLayoutPlot"))
        self.gridLayout.addLayout(self.verticalLayoutPlot, 4, 0, 1, 4)
        SpatialPlot.setWidget(self.dockWidgetContents)

        self.retranslateUi(SpatialPlot)
        QtCore.QMetaObject.connectSlotsByName(SpatialPlot)

    def retranslateUi(self, SpatialPlot):
        SpatialPlot.setWindowTitle(_translate("SpatialPlot", "Spatial Plot", None))
        self.label_3.setText(_translate("SpatialPlot", "Available Attributes", None))
        self.label_4.setText(_translate("SpatialPlot", "Y Axis Attributes", None))
        self.pushButtonAdd.setText(_translate("SpatialPlot", ">>", None))
        self.pushButtonRemove.setText(_translate("SpatialPlot", "<<", None))
        self.label_2.setText(_translate("SpatialPlot", "X Axis Attribute", None))

