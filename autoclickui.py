import sys, pyautogui
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial

class parent(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        self.x, self.y = 0, 0


class mainWindow(parent):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        # ------------ spinboxes ------------ #
        self.xcoord = spinBox()
        self.ycoord = spinBox()
        self.duration = spinBox()
        self.frequency = spinBox()

        # ------------ labels ------------ #
        self.xLabel = QtWidgets.QLabel('X Coordinate')
        self.yLabel = QtWidgets.QLabel('Y Coordinate')
        self.durLabel = QtWidgets.QLabel('Duration')
        self.freqLabel = QtWidgets.QLabel('Frequency')

        # ------------ buttons ------------ #
        self.coordBtn = QtWidgets.QPushButton('Get Coordinates')
        self.coordBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.okBtn = QtWidgets.QPushButton('OK')
        self.cancelBtn = QtWidgets.QPushButton('Cancel')

        # ------------ tooltips ------------ #
        self.xLabel.setToolTip('Set x position of mouse')
        self.yLabel.setToolTip('Set y position of mouse')
        self.durLabel.setToolTip('Set how many minutes to activate the clicker')
        self.freqLabel.setToolTip('Set how many times per minute to click')

        # ------------ grid ------------ #
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.xLabel, 1, 0)
        grid.addWidget(self.xcoord, 1, 1)

        grid.addWidget(self.yLabel, 2, 0)
        grid.addWidget(self.ycoord, 2, 1)

        grid.addWidget(self.coordBtn, 1, 2, 2, 1)

        grid.addWidget(self.durLabel, 3, 0)
        grid.addWidget(self.duration, 3, 1)

        grid.addWidget(self.freqLabel, 4, 0)
        grid.addWidget(self.frequency, 4, 1)

        grid.addWidget(self.okBtn, 5, 0, 1, 2)
        grid.addWidget(self.cancelBtn, 5, 2)

        self.setLayout(grid)

        # ------------ window properties ------------ #
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Auto Clicker')

        self.thread = QtCore.QThread(self)
        self.thread.setTerminationEnabled(True)

        # ------------ button connection ------------ #
        self.coordBtn.clicked.connect(self.coordScreen)
        self.okBtn.clicked.connect(self.threadConnect)
        self.cancelBtn.clicked.connect(self.abortThread)


    # ------------ button functions ------------ #
    
    # ------------ show overlay ------------ #
    @QtCore.pyqtSlot()
    def coordScreen(self):
        self.overlay = Overlay()
        self.overlay.show()
        self.overlay.xc.connect(self.updateX)
        self.overlay.yc.connect(self.updateY)

    # ------------ threading autoclick function ------------ #
    def threadConnect(self):
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(partial(self.worker.autoClick, self.duration.value(), self.frequency.value(), self.xcoord.value(), self.ycoord.value()))
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    # ------------ threading abort function ------------ #
    def abortThread(self):
        self.worker.abort = True

    # ------------ update coordinates ------------ #
    
    def updateX(self, xc):
        self.xcoord.setValue(xc)
    
    def updateY(self, yc):
        self.ycoord.setValue(yc)


# ------------ worker class / autoclick function ------------ #
class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.abort = False
    @QtCore.pyqtSlot()
    def autoClick(self, dur, freq, x, y):
        for _ in range(dur):
            for __ in range(freq):
                pyautogui.click(x, y, 1, 60/freq)
                if self.abort == True:
                    break
            if self.abort == True:
                break
        self.finished.emit()

# ------------ Overlay Label ------------ #
class OverlayLabel(QtWidgets.QLabel):
     
    def __init__(self):
        super().__init__()  
        self.setMouseTracking(True)
        self.setTextLabelPosition(0, 0)
        self.setAlignment(QtCore.Qt.AlignCenter)


    def mouseMoveEvent(self, eventQMouseEvent):
        self.setTextLabelPosition(eventQMouseEvent.x(), eventQMouseEvent.y())
        QtWidgets.QWidget.mouseMoveEvent(self, eventQMouseEvent)

    def setTextLabelPosition(self, x, y):
        self.x, self.y = x, y
        self.setText(f'Please click on the screen *avoid the corners* ({self.x}, {self.y})')



# ------------ Overlay ------------ #
class Overlay(parent):
    xc = QtCore.pyqtSignal(int)
    yc = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.4)
        self.label = OverlayLabel()
        layoutQHBoxLayout = QtWidgets.QHBoxLayout()
        layoutQHBoxLayout.addWidget(self.label)    
        self.setLayout(layoutQHBoxLayout)
        self.showFullScreen()
        

    def mousePressEvent(self, eventQMouseEvent):
        if eventQMouseEvent.button() == QtCore.Qt.LeftButton:
            self.x = self.label.x
            self.y = self.label.y
            self.xc.emit(self.x)
            self.yc.emit(self.y)
            
            self.close()

# ------------ spinbox class ------------ #
class spinBox(QtWidgets.QSpinBox):

    def __init__(self):
        super().__init__()
        
        self.setMaximum(10000)
        self.resize(self.sizeHint())


# ------------ main ------------ #
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

