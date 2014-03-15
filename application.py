#!/usr/bin/env python

import PySide
from PySide import QtCore, QtGui
import pyqtgraph as pg
import application_rc
from ui import Ui_FlashPower


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.curFile = ''
        self.ui = QtGui.QWidget()
        Ui_FlashPower().setupUi(self.ui)
        self.setCentralWidget(self.ui)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.setCurrentFile('')
        self.setUnifiedTitleAndToolBarOnMac(True)

    def maybeSave(self):
      return True

    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        if self.maybeSave():
            #self.textEdit.clear()
            self.setCurrentFile('')

    def open(self):
        if self.maybeSave():
            fileName, filtr = QtGui.QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)

    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def about(self):
        QtGui.QMessageBox.about(
            self,
            "About gl-power",
            "The <b>gl-power</b> example demonstrates how to write "
            "modern GUI applications using Qt, with a menu bar, "
            "toolbars, and a status bar.")


    def createActions(self):
        self.newAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'), "&New",
                                    self, shortcut=QtGui.QKeySequence.New,
                                    statusTip="Create a new file",
                                    triggered=self.newFile)

        self.openAct = QtGui.QAction(
            QtGui.QIcon(':/images/open.png'), '&Open...', self,
            shortcut=QtGui.QKeySequence.Open,
            statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QtGui.QAction(
            QtGui.QIcon(':/images/save.png'), '&Save', self,
            shortcut=QtGui.QKeySequence.Save,
            statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QtGui.QAction(
            'Save &As...', self, shortcut=QtGui.QKeySequence.SaveAs,
            statusTip="Save the document under a new name",
            triggered=self.saveAs)

        self.exitAct = QtGui.QAction(
            'E&xit', self, shortcut="Ctrl+Q", statusTip="Exit the application",
            triggered=self.close)

        self.aboutAct = QtGui.QAction(
            '&About', self, statusTip="Show the application's About box",
            triggered=self.about)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QtCore.QSettings("gan0ling Studio", "gl-power")
        pos = settings.value("pos", QtCore.QPoint(200, 200))
        size = settings.value("size", QtCore.QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QtCore.QSettings("gan0ling Studio", "gl-power")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(
                self, "gl-power", "Cannot read file %s:\n%s." % (
                    fileName, file.errorString()))
            return

        inf = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(
                self, "gl-power", "Cannot write file %s:\n%s." % (
                    fileName, file.errorString()))
            return False

        outf = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        #outf << self.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        #self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.txt'

        self.setWindowTitle("%s[*] - gl-power" % shownName)

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
