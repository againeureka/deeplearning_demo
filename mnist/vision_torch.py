#!/usr/bin/env python

'''
 - by J. Park,
 - history
    2021-06-08A : keras version
    2022-10-15A : torch version
'''

import math

from PyQt5.QtCore import Qt, pyqtSlot #, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QPushButton, QToolButton, QWidget, QCheckBox, QGroupBox, 
        QHBoxLayout, QStackedWidget,
        # QSlider, QScrollBar,QDial, QBoxLayout,
        QLabel, QSpinBox, QComboBox )
from PyQt5.QtGui import (QIcon)
import numpy as np

#from keras.preprocessing.image import load_img, img_to_array
#from keras.models import load_model

APP_TITLE = "Image Pad (by JPark@KETI, 2021-06)"

BLK_SIZE = 42

ROWS = 14
COLS = ROWS
R = np.zeros(ROWS)
ONES = np.ones(ROWS)
M = np.array( [ROWS, COLS])

class Puzzle(QWidget):
    nRows = ROWS
    nCols = COLS
    NumDigitButtons = nRows * nCols + 1
    
    def __init__(self, parent=None):
        super(Puzzle, self).__init__(parent)
        
        self.createControls("Settings")
        self.stackedWidget = QStackedWidget()
        #self.stackedWidget.addWidget(self.horizontalSliders)
        #self.horizontalSliders.valueChanged.connect(self.valueSpinBox.setValue)
        self.numIndexSpinBox.valueChanged.connect(self.drawNumber)
        self.valueSpinBox.valueChanged.connect(self.resizeBlk)

        self.solution = ''
        
        # solution button
        self.findSolutionButton = self.createButton(u"Find Solution", self.findSolutionClicked)

        # toggle buttons
        for i in range(Puzzle.NumDigitButtons):
            self.digitButtons.append(self.createToggleButton(str(i), self.digitClicked))

        # option checkbox
        self.optSolution = self.createCheckBox("show solution")
        self.optForWhite = self.createCheckBox("for white")

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        '''
        disp = self.initDisplay()
        mainLayout.addWidget(disp, 0, 0, 1, 2)
        #mainLayout.addWidget(self.findSolutionButton, 0, 4)
        mainLayout.addWidget(self.optSolution, 0, 2)
        mainLayout.addWidget(self.optForWhite, 0, 3)
        '''

        for i in range(0, Puzzle.NumDigitButtons-1):
            #row = ((9 - i) / 3) + 2
            #column = ((i - 1) % 3) + 1
            row = i / self.nRows + 1
            col =  i % self.nCols
            mainLayout.addWidget(self.digitButtons[i], row, col)

        #self.setLayout(mainLayout)
        self.setWindowTitle(APP_TITLE)

        layout = QHBoxLayout()
        layout.addWidget(self.controlsGroup)
        #layout.addWidget(self.stackedWidget)
        layout.addLayout(mainLayout)
        self.setLayout(layout)

        self.numIndexSpinBox.setValue(0)
        self.minimumSpinBox.setValue(0)
        self.maximumSpinBox.setValue(50)
        self.valueSpinBox.setValue(BLK_SIZE)

        self.optToggleAction = False
        self.optPenColor = False
        self.optDrawAction = False

        self.resetGame()
        self.findSolutionClicked()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_C:
            self.cleanPad()
        if e.key() == Qt.Key_S or e.key() == Qt.Key_P:
            n = self.predictNum()
            self.updateDisplay(n)
        elif e.key() == Qt.Key_T:
            self.optDrawAction = False
            self.optToggleAction = not self.optToggleAction
        elif e.key() == Qt.Key_D:
            self.optToggleAction = False
            self.optDrawAction = not self.optDrawAction
        elif e.key() == Qt.Key_W or e.key() == Qt.Key_B:
            self.optPenColor = not self.optPenColor
            self.optDrawAction = True
            self.optToggleAction = False

        self.cbToggleAction.setChecked(self.optToggleAction)
        self.cbDrawAction.setChecked(self.optDrawAction)
        self.cbPenColor.setChecked(self.optPenColor)
    def drawNumber(self, num):
        print('number = ', num)

        if (num > -1) and (num < 10):
            fname = str(num)+'.png'
            print('fname = ', fname)
            img = self.load_image(fname) # 14x14
            img = img.reshape(14*14,1)
        else:
            img = np.zeros(14*14)

        for idx, val in enumerate(img):
            state = True
            if val > 0.0:
                #self.digitButtons[idx].slot_toggle(True)
                state = True
            else:
                #self.digitButtons[idx].slot_toggle(False)
                state = False
            
            self.digitButtons[idx].setState(state)
    
        self.resize(100, 100)

        # number prediction
        n = self.predictNum()
        self.updateDisplay(n)

    def resizeBlk(self, size):
        # print('size = ', size)
        for idx in range(0, self.NumDigitButtons-1):
            self.digitButtons[idx].resizeBlk(size)
    
        self.resize(100, 100)

    def createCheckBox(self, text):
        checkBox = QCheckBox(text)
        checkBox.clicked.connect(self.findSolutionClicked)
        return checkBox

    def initDisplay(self):
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(35)

        # solution display
        font = self.display.font()
        font.setPointSize(font.pointSize() + 10)
        self.display.setFont(font)
        self.digitButtons = []

        return self.display

    def updateDisplay(self, s):
        
        self.display.setText(str(s))
        #if self.optSolution.isChecked(): 
        #    self.display.setText(str(s))
        #else:
        #    self.display.setText('Try please ...')

    def updateIcon(self, Y):
        return

        # notice, too time consumming
        for idx, val in enumerate(Y):
            button = self.digitButtons[idx]
            if(val > 0):
                button.setIcon(QIcon('white.png')) 
        
            else:
                button.setIcon(QIcon('black.png'))
            
            #self.setStyleSheet("background-color: %s" % ({True: "white", False: "black"}[val>0]))

    def getCurrentToggles(self):
        Y = []
        for idx in range(0, self.NumDigitButtons-1):
            Y.append( int(self.digitButtons[idx].getState()) )
        Y = np.array(Y)
 
        #self.updateIcon(Y)
        return Y

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def createToggleButton(self, text, member):
        button = ToggleButton(text)
        button.clicked.connect(member)
        return button

    def digitClicked(self):
        clickedButton = self.sender()
        clickedButton.clickToggle()
        #n = self.predictNum()
        #self.updateDisplay(n)
   
    # TODO, random으로 수정할 것 
    def resetGame(self):
        m = R
        print('m = ', m)
        for idx, i in enumerate(m):
            if ( i > 0 ):
                self.digitButtons[idx].toggle()

    def findSolutionClicked(self):
        Y = self.getCurrentToggles()

        if self.optForWhite.isChecked():
            Y = ONES - Y
        
    # load and prepare the image
    def load_image(self, filename):
        '''
        # load the image
        img = load_img(filename, grayscale=True, target_size=(28, 28))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 1 channel
        img = img.reshape(1, 28, 28, 1)
        # prepare pixel data
        img = img.astype('float32')
        #img = img / 255.0

        img = img.reshape(28, 28)
        img = img[::2, ::2] # downsampling 1/2
        img = img > 1
        img = img.astype(int)

        return img
        '''

        return None

    # load an image and predict the class
    def predictNum(self):
        img = self.getCurrentToggles()
        print('img = ', img)
        print('img.shape = ', img.shape)
        print('type(img) = ', type(img))

        img = img.reshape(ROWS, ROWS)

        #img = np.ones([28, 28])  * 0.5
        #img = img[::2, ::2] # downsampling
        img = img.repeat(2, axis=0).repeat(2, axis=1) # upsampling
        
        img = img.reshape(1,28,28,1)

        '''
        model = load_model('handwritten_binary_epoch15.h5')
        #model = load_model('handwritten_binary_aug.h5')
        
        # predict the class
        digit = model.predict_classes(img)
        print('predicted value = ', digit[0])
        return digit[0]
        '''
        return 0

    def createControls(self, title):
        self.controlsGroup = QGroupBox(title)

        helpLabel = QLabel("[c,d]:drawing, [s,p]:prediction")
        numIndexLabel = QLabel("number:")
        minimumLabel = QLabel("size min:")
        maximumLabel = QLabel("size max:")
        valueLabel = QLabel("size:")

        self.cbToggleAction = QCheckBox("toggle pen")
        self.cbDrawAction = QCheckBox("draw")
        self.cbPenColor = QCheckBox("white pen")
        
        self.cbPenColor.setChecked(True)
        self.cbToggleAction.setChecked(False)
        self.cbDrawAction.setChecked(False)

        self.numIndexSpinBox = QSpinBox()
        self.numIndexSpinBox.setRange(-1, 9)
        self.numIndexSpinBox.setSingleStep(1)

        self.minimumSpinBox = QSpinBox()
        self.minimumSpinBox.setRange(1, 100)
        self.minimumSpinBox.setSingleStep(1)

        self.maximumSpinBox = QSpinBox()
        self.maximumSpinBox.setRange(1, 100)
        self.maximumSpinBox.setSingleStep(1)

        self.valueSpinBox = QSpinBox()
        self.valueSpinBox.setRange(1, 100)
        self.valueSpinBox.setSingleStep(1)

        orientationCombo = QComboBox()
        orientationCombo.addItem("Horizontal slider-like widgets")
        #orientationCombo.addItem("Vertical slider-like widgets")

        #orientationCombo.activated.connect(self.stackedWidget.setCurrentIndex)
        #self.minimumSpinBox.valueChanged.connect(self.horizontalSliders.setMinimum)
        #self.minimumSpinBox.valueChanged.connect(self.verticalSliders.setMinimum)
        #self.maximumSpinBox.valueChanged.connect(self.horizontalSliders.setMaximum)
        #self.maximumSpinBox.valueChanged.connect(self.verticalSliders.setMaximum)
        self.cbToggleAction.toggled.connect(self.setToggleAction)
        self.cbDrawAction.toggled.connect(self.setDrawAction)
        self.cbPenColor.toggled.connect(self.setPenColor)
        #invertedAppearance.toggled.connect(self.verticalSliders.invertAppearance)
        #invertedKeyBindings.toggled.connect(self.horizontalSliders.invertKeyBindings)
        #invertedKeyBindings.toggled.connect(self.verticalSliders.invertKeyBindings)

        controlsLayout = QGridLayout()
    
        disp = self.initDisplay()
        controlsLayout.addWidget(disp, 0, 0, 1, 2)


        controlsLayout.addWidget(numIndexLabel, 1, 0)
        controlsLayout.addWidget(self.numIndexSpinBox, 1, 1)

        controlsLayout.addWidget(self.cbToggleAction, 2, 0)
        controlsLayout.addWidget(self.cbDrawAction, 2, 1)
        controlsLayout.addWidget(self.cbPenColor, 2, 2)

        controlsLayout.addWidget(minimumLabel, 3, 0)
        controlsLayout.addWidget(self.minimumSpinBox, 3, 1)

        controlsLayout.addWidget(maximumLabel, 4, 0)
        controlsLayout.addWidget(self.maximumSpinBox, 4, 1)

        controlsLayout.addWidget(valueLabel, 5, 0)
        controlsLayout.addWidget(self.valueSpinBox, 5, 1)
        #controlsLayout.addWidget(invertedKeyBindings, 1, 2)
        #controlsLayout.addWidget(orientationCombo, 3, 0, 1, 3)

        controlsLayout.addWidget(helpLabel, 6, 0)

        self.controlsGroup.setLayout(controlsLayout)

    def setToggleAction(self):
        if self.cbToggleAction.isChecked():
            for idx in range(0, self.NumDigitButtons-1):
                self.digitButtons[idx].setToggleAction(self.optToggleAction)
    
    def setDrawAction(self):
        for idx in range(0, self.NumDigitButtons-1):
            self.digitButtons[idx].setDrawAction(self.optDrawAction)
        
    def setPenColor(self):
        '''
        if self.cbPenColor.isChecked():
            self.optPenColor = True
        else:
            self.optPenColor = False
        '''
        if self.optDrawAction:
            for idx in range(0, self.NumDigitButtons-1):
                self.digitButtons[idx].setPenColor(self.optPenColor)
        
    def cleanPad(self):
        self.optToggleAction = False
        self.optDrawAction = False
        self.cbToggleAction.setChecked(self.optToggleAction)
        self.cbDrawAction.setChecked(self.optDrawAction)

        for idx in range(0, self.NumDigitButtons-1):
            self.digitButtons[idx].setState(False)


class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 10)
        size.setWidth(max(size.width(), size.height()))
        return size

class ToggleButton(QPushButton):
    def __init__(self, text, parent=None):
        super(ToggleButton, self).__init__(parent)

        self.blkWidth = 35
        self.blkHeight = 35
        
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.setText(text)

        QPushButton.__init__(self, text)
        self.setFixedSize(self.blkWidth, self.blkHeight)
        self.setStyleSheet("background-color: black")

        self.setCheckable(False)
        self.toggled.connect(self.slot_toggle)
        self.state = False
        self.optToggleAction = False
        self.optDrawAction = False
        self.optPenColor = True

    def setToggleAction(self, value = False):
        self.optToggleAction = value

    def setDrawAction(self, value = False):
        self.optDrawAction = value

    def setPenColor(self, value = False):
        self.optPenColor = value # white or black

    def enterEvent(self, QEvent):
        # here the code for mouse hover
        if self.optToggleAction:
            self.clickToggle()
        elif self.optDrawAction:
            self.setState(self.optPenColor)

    def leaveEvent(self, QEvent):
        # here the code for mouse leave
        pass

    def resizeBlk(self, size):
        self.blkWidth = size
        self.blkHeight = size
        self.setFixedSize(self.blkWidth, self.blkHeight)

    def sizeHint(self):
        size = super(ToggleButton, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

    def clickToggle(self):
        self.state = not self.state
        self.slot_toggle(self.state)
    
    @pyqtSlot(bool)
    def slot_toggle(self, state):
        #digitValue = int(self.text())
        #print('digitValue = ', digitValue)
        self.state = state
        #self.setIcon(QIcon('white.png')) 
        #self.setIcon(QIcon('black.png'))
        self.setStyleSheet("background-color: %s" % ({True: "white", False: "black"}[state]))
        #self.setText({True: "ON", False: "OFF"}[state])

    def setState(self, state):
        self.state = bool(state)
        self.setStyleSheet("background-color: %s" % ({True: "white", False: "black"}[state]))
        self.slot_toggle(self.state)

    def getState(self):
        return self.state


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = Puzzle()
    calc.show()
    sys.exit(app.exec_())
