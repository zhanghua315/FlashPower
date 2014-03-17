# -- coding: utf-8 --

from PySide import QtCore, QtGui
import pyqtgraph as pg
import application_rc
from ui import Ui_FlashPower
import numpy as np
import numexpr as ne
import logbook


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.enable_log = False
        self.log = logbook.Logger('MainWindow')
        self.curFile = ''
        self.ui = Ui_FlashPower()
        self.ui.setupUi(self.ui)
        self.setCentralWidget(self.ui)
        self.contextMenu = None
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.pointStack = []
        self.precision = 3  # 时间最小分辨率，默认为3（1ms）。
        self.readSettings()
        self.modified = False

        self.setCurrentFile('')
        self.setUnifiedTitleAndToolBarOnMac(True)

        #init plot 
        self.desiredPlot = self.ui.mainplot.plot(name=u'期望值')
        self.desiredPlot.curve.setClickable(True)
        self.actualPlot = self.ui.mainplot.plot(name=u'实际值')
        self.desiredPlot.setPen((0,255,0))
        self.actualPlot.setPen((255,0,0))
        self.clickedX = []
        self.clickedY = []
        self.strFunc  = []
        self.x_output = []
        self.y_output = []
        self.eventPos = None
        self.curArrow = pg.ArrowItem(pos=(0, 0), angle=-45)
        self.ui.mainplot.addItem(self.curArrow)
        

        #connect signal to slot
        self.ui.cmd_lineedit.returnPressed.connect(self.on_editingFinished)
        self.ui.graphWin.scene().sigMouseMoved.connect(self.mouse_moved)
        self.ui.graphWin.scene().sigMouseClicked.connect(self.mouse_clicked)

    def maybeSave(self):
        if self.modified:
            ok = QtGui.QMessageBox.warning(self,self.tr("Warning"), self.tr("Save current file??"),
                                      QtGui.QMessageBox.Save,QtGui.QMessageBox.Cancel)
            if ok == QtGui.QMessageBox.Save:
                return True
            else :
                return False

    def closeEvent(self, event):
        if self.maybeSave():
            self.save()
            self.writeSettings()
        event.accept()

    def newFile(self):
        if self.maybeSave():
            self.save()
        self.modified = False
        self.clickedX = []
        self.clickedY = []
        self.x_output = []
        self.y_output = []
        self.desiredPlot.clear()
        self.actualPlot.clear()
        self.setCurrentFile('')

    def open(self):
        if self.maybeSave():
            self.modified = False
            self.clickedX = []
            self.clickedY = []
            self.x_output = []
            self.y_output = []
            self.desiredPlot.clear()
            self.actualPlot.clear()
            self.save()
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

    def back(self):
        try:
            x = self.clickedX.pop()
            y = self.clickedY.pop()
            self.pointStack.append((x,y))
            self.desiredPlot.setData(self.clickedX,self.clickedY)
            self.curArrow.setPos(x,y)
        except IndexError:
            self.log.warn("undo:pop from  a empty list")

    def forward(self):
        try:
            x,y = self.pointStack.pop()
            self.clickedX.append(x)
            self.clickedY.append(y)
            self.desiredPlot.setData(self.clickedX,self.clickedY)
            self.curArrow.setPos(x,y)
        except IndexError:
            self.log.warn("redo,stack empty.no data to redo")

    def createOutputWave(self):
        """
            根据用户点击的坐标点生成最终的输出波形
        """
        self.x_output = []
        self.y_output = []
        if self.precision == 3:
            precision = 0.001
        if self.precision == 4:
            precision = 0.0001
        else:
            precision = 0.001
        for i in range(len(self.clickedX)-1):
            x = np.arange(start=self.clickedX[i],stop=self.clickedX[i+1],step=precision)
            self.x_output = np.append(self.x_output,x)
            y = ne.evaluate(self.strFunc[i])
            self.y_output = np.append(self.y_output,y)
        

    def begin(self):
        #TODO add Begin Logic
        if len(self.clickedX) >= 2:
            self.createOutputWave()
            self.desiredPlot.setData(self.x_output,self.y_output)
            #TODO send data into device and send start cmd
            #TODO start update thread
        else :
            self.statusBar().showMessage("not enough data to output.must >= 2 points",2000)

    def stop(self):
        #TODO send stop cmd
        #TODO stop updata thread
        pass

    def switchLog(self):
        self.enable_log = not self.enable_log
        if self.enable_log:
            self.log.level = logbook.DEBUG
            self.statusBar().showMessage("Log On",2000)
        else:
            self.log.level = logbook.ERROR
            self.statusBar().showMessage("Log Off",2000)
        

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

        self.beginAct = QtGui.QAction(QtGui.QIcon(':/images/begin.png'),
                                      "&Begin",self,statusTip="Begin output",triggered=self.begin)
        self.stopAct = QtGui.QAction(QtGui.QIcon(':/images/stop.png'),
                                     "S&top",self,statusTip="Stop output",triggered=self.stop)
        self.logAct  = QtGui.QAction("&Log",self,statusTip="Start/Stop Log",triggered=self.switchLog)
        self.backAct = QtGui.QAction(QtGui.QIcon(":/images/back.png"),"Undo",self,
                                     shortcut=QtGui.QKeySequence.Undo,statusTip="Undo insert output point",
                                     triggered=self.back)
        self.forwardAct = QtGui.QAction(QtGui.QIcon(":/images/forward.png"),"Redo",self,
                                     shortcut=QtGui.QKeySequence.Redo,statusTip="Redo insert output point",
                                     triggered=self.forward)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.beginAct)
        self.fileMenu.addAction(self.stopAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.logAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        ########################################
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.backAct)
        self.editMenu.addAction(self.forwardAct)
        ########################################
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.backAct)
        self.fileToolBar.addAction(self.forwardAct)
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.beginAct)
        self.fileToolBar.addAction(self.stopAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QtCore.QSettings("gan0ling Studio", "gl-power")
        pos = settings.value("pos", QtCore.QPoint(200, 200))
        size = settings.value("size", QtCore.QSize(400, 400))
        self.enable_log = settings.value("enable-log",False)
        if self.enable_log:
            self.log.level = logbook.DEBUG
        else :
            self.log.level = logbook.ERROR
        self.resize(size)
        self.move(pos)
        

    def writeSettings(self):
        settings = QtCore.QSettings("gan0ling Studio", "gl-power")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())
        settings.setValue("enable-log",self.enable_log)

    def loadFile(self, fileName):
        #TODO add logic
        npzfile = np.load(fileName)
        if len(npzfile.files) >= 4:
            self.clickedX = npzfile['clickedX']
            self.clickedY = npzfile['clickedY']
            self.x_output = npzfile['x_output']
            self.y_output = npzfile['y_output']
            self.desiredPlot.setData(self.x_output,self.y_output)
            self.statusBar().showMessage("File loaded", 2000)
        else :
            self.statusBar().showMessage("File corrupted or no data",2000)

    def saveFile(self, fileName):
        #TODO add logic
        self.createOutputWave()
        np.savez_compressed(fileName,clickedX=self.clickedX,clickedY=self.clickedY,
                            x_output=self.x_output,y_output=self.y_output)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.setWindowModified(False)

        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.npz'

        self.setWindowTitle("%s[*] - gl-power" % shownName)

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()

    #Slot Funciton
    def on_editingFinished(self):
        #TODO add send cmd logic
        print "edit finish"

    def setCurve(self):
        if self.eventPos is not None:
            if len(self.clickedX) >= 2:
                posX = self.eventPos.x()
                posY = self.eventPos.y()
                idx  = 0
                #查找鼠标右键位置在用户点击的点序列中的位置
                for i in range(len(self.clickedX)):
                    if (self.clickedX[i] <= posX) and (self.clickedX[i+1] >= posX):
                        idx = i
                        break
                if (idx == 0) and (i != 0):
                    #用户点击位置下，还没有设置输出点
                    return
                #找到需要更改斜率的线段，调用QInputDialog让用户输入函数
                text = QtGui.QInputDialog.getText(self,self.tr(u"Function expression"),
                                                  self.tr("y = "),QtGui.QLineEdit.Normal,
                                                  "cos(x)")
                if text[1] and text[0] and ("x" in text[0]):
                    func = str(text[0]) + " + " +str(self.clickedY[idx])
                    self.strFunc[i] = func
                
                

    def mouse_moved(self, event):
        pos = event
        if self.ui.mainplot.sceneBoundingRect().contains(pos):
            mousePoint = self.ui.mainplot.vb.mapSceneToView(pos)
            self.ui.label.setText("<span style='font-size: 12pt'>X:%0.4f   "
                                  "<span style='color:green'>  Y1:%0.4f</span> " #TODO change y1,y2 value
                                  "<span style='color:red'>  Y2:%0.4f</span>"
                                  % (mousePoint.x(),mousePoint.y(),mousePoint.y()))
            self.ui.vLine.setPos(mousePoint.x())
            self.ui.hLine.setPos(mousePoint.y())

    def addOutputPoint(self,x,y):
        self.modified = True
        self.clickedX.append(x)
        self.clickedY.append(y)
        if len(self.clickedX) >= 2:
            ratio = (self.clickedY[-1] - self.clickedY[-2]) / (self.clickedX[-1] - self.clickedX[-2])
            # y= y[-2] + (y[-1]-y[-2])/(x[-1]-x[-2]) * (x-x[-2])
            ratio = str(self.clickedY[-2])+" + "+str(ratio) + " * (x - " + str(self.clickedX[-2]) + ")"
            self.strFunc.append(ratio)
        self.curArrow.setPos(x,y)

    def mouse_clicked(self, event):
        if event.button() == QtCore.Qt.LeftButton and event.double():
            mousePoint = self.ui.mainplot.vb.mapSceneToView(event.scenePos())
            x = round(mousePoint.x(),self.precision)
            y = round(mousePoint.y(),self.precision)
            #第一次点击的检查
            if len(self.clickedX) == 0 and x != 0:
                self.statusBar().showMessage("x value of first point must be zero!!",2000)
                self.log.warn("mouse_cliked:x value of first point must be zero!!",2000)
                return 
            if len(self.clickedX) !=0 and (x <= self.clickedX[-1]):
                self.statusBar().showMessage("invalid point",2000)
                return
            else:
                self.addOutputPoint(x,y)
                self.desiredPlot.setData(self.clickedX,self.clickedY)
            event.accept()
        elif event.button() == QtCore.Qt.RightButton:
            if self.raiseContextMenu(event):
                self.eventPos = self.ui.mainplot.vb.mapSceneToView(event.scenePos())
                event.accept()


    def raiseContextMenu(self, ev):
        menu = self.getMenu(ev)
        if menu is None:
            return False
        menu = self.ui.mainplot.scene().addParentContextMenus(self.ui.mainplot.vb, menu, ev)
        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))
        return True

    def getMenu(self,event):
        #if self.contextMenu is None:
        self.contextMenu = self.ui.mainplot.vb.getMenu(event)
        self.curveAct = QtGui.QAction("set curve",self.contextMenu)
        self.curveAct.triggered.connect(self.setCurve)
        self.contextMenu.addAction(self.curveAct)
        self.contextMenu.curveAct = self.curveAct
        return self.contextMenu




if __name__ == '__main__':

    import sys
    from logbook import FileHandler
    
    log_handler = FileHandler("FlashPower.log")
    with log_handler.applicationbound():
        app = QtGui.QApplication(sys.argv)
        mainWin = MainWindow()
        mainWin.show()
        sys.exit(app.exec_())
