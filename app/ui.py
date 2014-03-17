# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'application.ui'
#
# Created: Sat Mar 15 16:08:09 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import pyqtgraph as pg

class Ui_FlashPower(QtGui.QWidget):
    def setupUi(self, FlashPower):
        FlashPower.setObjectName("FlashPower")
        FlashPower.resize(756, 408)
        self.gridLayout = QtGui.QGridLayout(FlashPower)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(FlashPower)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(179, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.voltage_lcd = QtGui.QLCDNumber(FlashPower)
        self.voltage_lcd.setProperty("value", 12.2)
        self.voltage_lcd.setObjectName("voltage_lcd")
        self.horizontalLayout_2.addWidget(self.voltage_lcd)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(FlashPower)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.tempature_lcd = QtGui.QLCDNumber(FlashPower)
        self.tempature_lcd.setProperty("value", 12.2)
        self.tempature_lcd.setObjectName("tempature_lcd")
        self.horizontalLayout_3.addWidget(self.tempature_lcd)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 4, 1, 1)
        self.graphWin = pg.GraphicsWindow()
        self.label = pg.LabelItem(justify='right')
        self.graphWin.addItem(self.label)
        self.mainplot = self.graphWin.addPlot(row=1,col=0)
        self.mainplot.setYRange(0,30)
        self.mainplot.showGrid(True,True,0.5)
        self.mainplot.setLabel('left','Voltage',units='V')
        self.mainplot.setLabel('bottom','Time',units='S')
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.mainplot.addItem(self.vLine,ignoreBounds=True)
        self.mainplot.addItem(self.hLine,ignoreBounds=True)
        self.mainplot.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphWin, 1, 0, 1, 5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtGui.QLabel(FlashPower)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.cmd_lineedit = QtGui.QLineEdit(FlashPower)
        self.cmd_lineedit.setObjectName("cmdlineedit")
        self.horizontalLayout.addWidget(self.cmd_lineedit)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtGui.QLabel(FlashPower)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.current_lcd = QtGui.QLCDNumber(FlashPower)
        self.current_lcd.setProperty("value", 12.2)
        self.current_lcd.setObjectName("current_lcd")
        self.horizontalLayout_4.addWidget(self.current_lcd)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)

        self.retranslateUi(FlashPower)

    def retranslateUi(self, FlashPower):
        FlashPower.setWindowTitle(
            QtGui.QApplication.translate("FlashPower", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(
            QtGui.QApplication.translate("FlashPower", "Voltage:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(
            QtGui.QApplication.translate("FlashPower", "Tempature:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FlashPower", "cmd:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(
            QtGui.QApplication.translate("FlashPower", "Current :", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    FlashPower = QtGui.QWidget()
    ui = Ui_FlashPower()
    ui.setupUi(FlashPower)
    FlashPower.show()
    sys.exit(app.exec_())

