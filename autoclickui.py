import sys, pyautogui
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial

class mainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        # ------------ spinboxes ------------ #
        self.x = spinBox()
        self.y = spinBox()
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
        grid.addWidget(self.x, 1, 1)

        grid.addWidget(self.yLabel, 2, 0)
        grid.addWidget(self.y, 2, 1)

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

        # ------------ button connection ------------ #
        self.coordBtn.clicked.connect(self.coordScreen)
        self.okBtn.clicked.connect(partial(self.autoclick, self.duration.value(), self.frequency.value(), self.x.value(), self.y.value()))


    # ------------ button functions ------------ #
    @QtCore.pyqtSlot()
    def coordScreen(self):
        self.coord = coordWindow()
        self.coord.show()
        self.x.setValue(self.coord.x)
        

    @QtCore.pyqtSlot()
    def autoclick(self, dur, freq, x, y):
        print(f'{dur}, {freq}, {x}, {y}')
        for minutes in range(dur):
            for period in range(freq):
                pyautogui.click(x, y, 1, 60/freq)

# ------------ Second Window Label ------------ #
class coordLabel(QtWidgets.QLabel):
     
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

# ------------ Second Window Overlay ------------ #
class coordWindow(QtWidgets.QWidget):
    def __init__(self, parent=mainWindow):
        super().__init__()
        self.setWindowOpacity(0.4)
        self.label = coordLabel()
        layoutQHBoxLayout = QtWidgets.QHBoxLayout()
        layoutQHBoxLayout.addWidget(self.label)    
        self.setLayout(layoutQHBoxLayout)
        self.showFullScreen()
        self.x, self.y = 0, 0

        self.w = parent

    def mousePressEvent(self, eventQMouseEvent):
        if eventQMouseEvent.button() == QtCore.Qt.LeftButton:
            print(f'{self.label.x}, {self.label.y}')
            self.x = self.label.x
            self.y = self.label.y
            print(f'{self.x}, {self.y}')

            
            self.close()


    
class spinBox(QtWidgets.QSpinBox):

    def __init__(self):
        super().__init__()
        
        self.setMaximum(10000)
        self.resize(self.sizeHint())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

