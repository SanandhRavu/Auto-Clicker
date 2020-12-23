import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton,
                             QMessageBox, QHBoxLayout, QVBoxLayout,
                             QTextEdit, QGridLayout, QLineEdit, QLabel, QSizePolicy, QSpinBox)
from PyQt5 import QtCore, QtGui
import pyautogui
from functools import partial


class Window(QWidget):

    def __init__(self):
        super().__init__()

        

        self.initUI()


    def initUI(self):
        QToolTip.setFont(QtGui.QFont('SansSerif', 10))


        # ---------- widgets ------------------------------
        
        self.xEdit = QSpinBox()
        self.xEdit.setMaximum(10000)
        self.yEdit = QSpinBox()
        self.yEdit.setMaximum(10000)

        self.duration = QLabel('Duration')
        self.frequency = QLabel('Frequency')
        self.xCoordinate = QLabel('X Coordinate')
        self.yCoordinate = QLabel('Y Coordinate')

        self.durationEdit = QSpinBox()
        self.frequencyEdit = QSpinBox()

        self.coordButton = QPushButton('Get Coordinates', self)
        self.okButton = QPushButton('OK', self)
        self.cancelButton = QPushButton('Cancel')


        # ---------- tooltips ------------------------------
        
        self.duration.setToolTip('Set how many minutes to activate the clicker')
        self.duration.resize(self.duration.sizeHint())

        self.frequency.setToolTip('Set how many times per minute to click')
        self.frequency.resize(self.frequency.sizeHint())

        self.xCoordinate.setToolTip('Set x position of mouse')
        self.xCoordinate.resize(self.xCoordinate.sizeHint())

        self.yCoordinate.setToolTip('Set y position of mouse')
        self.yCoordinate.resize(self.yCoordinate.sizeHint())

        # ---------- layout ------------------------------
        #
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.duration, 3, 0)
        grid.addWidget(self.durationEdit, 3, 1)
        

        grid.addWidget(self.frequency, 4, 0)
        grid.addWidget(self.frequencyEdit, 4, 1)

        grid.addWidget(self.xCoordinate, 1, 0)
        grid.addWidget(self.xEdit, 1, 1)

        grid.addWidget(self.yCoordinate, 2, 0)
        grid.addWidget(self.yEdit, 2, 1)

        self.coordButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addWidget(self.coordButton, 1, 2, 2, 1)


        grid.addWidget(self.okButton, 5, 0, 1, 2)
        grid.addWidget(self.cancelButton, 5, 2)


        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("Auto Clicker")

        self.durationEdit.update()
        self.frequencyEdit.update()
        

        # ---------- button connection ------------------------------
        
        self.coordButton.clicked.connect(self.coordScreen)
        self.okButton.clicked.connect(partial(self.autoclick, self.durationEdit.value(), self.frequencyEdit.value(), self.xEdit.value(), self.yEdit.value()))
        # self.okButton.clicked.connect(partial(self.autoclick, 1, 30, self.xEdit.value(), self.yEdit.value()))

        # ---------- misc ------------------------------
        
        # self.setWindowIcon()
        self.show()

    # ---------- buttons ------------------------------

    def coordScreen(self):
        global w 
        w = QCustomWidget()
        w.show()
        self.close()

    @staticmethod
    def autoclick(dur, freq, x, y):
        print(f'{dur}, {freq}, {x}, {y}')
        for minutes in range(dur):
            for period in range(freq):
                pyautogui.click(x, y, 1, 60/freq)
            
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Auto Clicker',
    #                                  'Are you sure you want to quit?', QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

# ---------- coordinates window ------------------------------

class QCustomLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setTextLabelPosition(0, 0)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def mouseMoveEvent(self, eventQMouseEvent):
        self.setTextLabelPosition(eventQMouseEvent.x(), eventQMouseEvent.y())
        QWidget.mouseMoveEvent(self, eventQMouseEvent)

    def mousePressEvent(self, eventQMouseEvent):
        self.win = Window()
        if eventQMouseEvent.button() == QtCore.Qt.LeftButton:
            self.win.xEdit.setValue(self.x)
            self.win.yEdit.setValue(self.y)
            self.win.xEdit.update()
            self.win.yEdit.update()
            w.close()
            
        QWidget.mousePressEvent(self, eventQMouseEvent)

    def setTextLabelPosition(self, x, y):
        self.x, self.y = x, y
        self.setText(f'Please click on the screen *avoid the corners* ({self.x} : {self.y} )')


class QCustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.4)
        # Init QLabel
        self.positionQLabel = QCustomLabel()
        # Init QLayout
        layoutQHBoxLayout = QHBoxLayout()
        layoutQHBoxLayout.addWidget(self.positionQLabel)
        self.setLayout(layoutQHBoxLayout)
        self.showFullScreen()


#---------- main ------------------------------

def main():

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
