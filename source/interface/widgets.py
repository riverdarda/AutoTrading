import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QIcon, QFont, QPalette, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, qApp, QTabWidget, 
    QHBoxLayout, QVBoxLayout, QLabel, QToolBar, QToolButton, QTextEdit,
    QScrollArea, QPushButton, QDesktopWidget, QComboBox, QGridLayout, QCheckBox,
    QLineEdit, QRadioButton, QScrollArea)

import re
import time
import thread
import os

from PyQt5.uic.properties import QtCore


class MainWindow(QMainWindow):

    def __init__(self, autoTradingSystem):

        super(MainWindow, self).__init__()
        self.ATM = autoTradingSystem
        self.initUI()

    def initUI(self):

        self.setStyle()
        self.setWindowTitle('Auto Trading System')
        self.initToolBar()
        self.initMenuBar()
        self.initMainBoard()
        self.techAnPage()
        #self.pairTrPage()

        # make window in center point
        self.setFixedSize(1000, 700)
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

        self.show()

    def initMainBoard(self):

        self.mainBoard = QWidget()
        self.setCentralWidget(self.mainBoard)
        self.pagesStatus = [0]*5
        self.pages = [QWidget(self.mainBoard) for i in self.pagesStatus]
        self.toolButtons

        self.mainBoard.setStyleSheet(self.mainBoardQSS)
        for page in self.pages: page.setStyleSheet(self.pagesQSS)

    def initToolBar(self):

        self.toolBar = QToolBar("Tools")
        self.toolBar.setMovable(False)
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        self.toolBar.setIconSize(QSize(20, 20))

        self.techAnButton = QToolButton()
        self.techAnButton.setText("Technical analysis")
        self.techAnButton.setFixedSize(130, 25)
        self.pairTrButton = QToolButton()
        self.pairTrButton.setText("Pair Trading")
        self.pairTrButton.setFixedSize(130, 25)
        self.atoTrdButton = QToolButton()
        self.atoTrdButton.setText("Monitor")
        self.atoTrdButton.setFixedSize(130, 25)
        self.trdPnlButton = QToolButton()
        self.trdPnlButton.setText("PnL Report")
        self.trdPnlButton.setFixedSize(130, 25)
        self.trdHisButton = QToolButton()
        self.trdHisButton.setText("Trade History")
        self.trdHisButton.setFixedSize(130, 25)

        self.techAnButton.clicked.connect(self.techAnPage)
        self.pairTrButton.clicked.connect(self.pairTrPage)
        self.atoTrdButton.clicked.connect(self.atoTrdPage)
        self.trdPnlButton.clicked.connect(self.trdPnlPage)
        self.trdHisButton.clicked.connect(self.trdHisPage)

        self.toolBar.addWidget(self.techAnButton)
        self.toolBar.addWidget(self.pairTrButton)
        self.toolBar.addWidget(self.atoTrdButton)
        self.toolBar.addWidget(self.trdPnlButton)
        self.toolBar.addWidget(self.trdHisButton)
        self.toolButtons = [self.techAnButton, self.pairTrButton, self.atoTrdButton, self.trdPnlButton, self.trdHisButton]

    def initMenuBar(self):

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        techAnAction = QAction('&Technical Analysis', self)
        techAnAction.setShortcut('Ctrl+T')
        techAnAction.triggered.connect(self.techAnPage)
        pairTrAction = QAction('&Pair Trading', self)
        pairTrAction.setShortcut('Ctrl+P')
        pairTrAction.triggered.connect(self.pairTrPage)
        atoTrdAction = QAction('&Monitor', self)
        atoTrdAction.setShortcut('Ctrl+M')
        atoTrdAction.triggered.connect(self.atoTrdPage)
        trdPnlAction = QAction('&Profit And Loss Report', self)
        trdPnlAction.setShortcut('Ctrl+R')
        trdPnlAction.triggered.connect(self.trdPnlPage)
        trdHisAction = QAction('&Trade History', self)
        trdHisAction.setShortcut('Ctrl+H')
        trdHisAction.triggered.connect(self.trdHisPage)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fannsMenu = menubar.addMenu('&App')
        fannsMenu.addAction(exitAction)
        naviMenu = menubar.addMenu('&Navigate')
        naviMenu.addAction(techAnAction)
        naviMenu.addAction(pairTrAction)
        naviMenu.addAction(atoTrdAction)
        naviMenu.addAction(trdPnlAction)
        naviMenu.addAction(trdHisAction)

    # The technical analysis page
    def techAnPage(self):

        # hide all pages to show self page
        for pi in range(0,len(self.pages)):
            self.toolButtons[pi].setStyleSheet(self.toolButtonHideQSS)
            self.pages[pi].hide()

        print "in technical analysis page"
        ci = 0
        page = self.pages[ci]
        self.toolButtons[ci].setStyleSheet(self.toolButtonFocusQSS)

        if self.pagesStatus[ci] == 0:

            self.pageTechAnConfigWidget = QWidget(page)
            self.pageTechAnConfigWidget.setFixedSize(860, 700)

            pageMainVerticalBox = QVBoxLayout()
            pageMainVerticalBox.setContentsMargins(0, 5, 0, 0)

            self.pageTechAnTitleLabel = QLabel("Technical Analysis", page)
            self.pageTechAnTitleLabel.setFixedSize(860, 25)
            self.pageTechAnTitleLabel.setStyleSheet(self.pageTitleQSS)
            pageMainVerticalBox.addWidget(self.pageTechAnTitleLabel)

            # capital config components
            self.pageTechAnCapitalLabel = QLabel("Capital Config", page)
            self.pageTechAnCapitalLabel.setFixedSize(860, 25)
            self.pageTechAnCapitalLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pageTechAnCapitalLabel)
            capitalHbox = QHBoxLayout()
            capitalHbox.setContentsMargins(30, 10, 0, 10)
            self.pageTechAnCapitalInputLabel = QLabel("Capital: ", page)
            self.pageTechAnCapitalInputLabel.setFont(self.contentFont)
            self.pageTechAnCapitalInputLabel.setFixedSize(100, 25)
            self.pageTechAnCapitalInputLabel.setStyleSheet(self.itemNameQSS)
            capitalHbox.addWidget(self.pageTechAnCapitalInputLabel)
            self.pageTechAnCapitalEdit = QLineEdit("$ 100,000,000")
            self.pageTechAnCapitalEdit.setStyleSheet(self.lineEditQSS)
            self.pageTechAnCapitalEdit.setFixedSize(300, 25)
            self.pageTechAnCapitalEdit.setEnabled(False)
            capitalHbox.addWidget(self.pageTechAnCapitalEdit)
            capitalHbox.addStretch(1)
            pageMainVerticalBox.addLayout(capitalHbox)

            # security code select components
            self.pageTechAnSecurityLabel = QLabel("Security Select", page)
            self.pageTechAnSecurityLabel.setFixedSize(860, 25)
            self.pageTechAnSecurityLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pageTechAnSecurityLabel)
            securityHbox = QHBoxLayout()
            securityHbox.setContentsMargins(30, 10, 0, 10)
            self.pageTechAnSecurityCode= QLabel("Security Code: ", page)
            self.pageTechAnSecurityCode.setFont(self.contentFont)
            self.pageTechAnSecurityCode.setFixedSize(100, 25)
            self.pageTechAnSecurityCode.setStyleSheet(self.itemNameQSS)
            securityHbox.addWidget(self.pageTechAnSecurityCode)
            self.pageTechAnSecurityCombo = QComboBox(page)
            self.pageTechAnSecurityCombo.setFixedSize(300, 25)
            self.pageTechAnSecurityCombo.setStyleSheet(self.comboQSS)
            self.pageTechAnSecurityCombo.addItem("hsi_futures_jan")
            for item in self.ATM.data.getAssetList("./dataManager/data/hsi_futures"): self.pageTechAnSecurityCombo.addItem(item)
            securityHbox.addWidget(self.pageTechAnSecurityCombo)
            securityHbox.addStretch(1)
            pageMainVerticalBox.addLayout(securityHbox)

            # investment strategies select components
            self.pageTechAnStrategiesLabel = QLabel("Investment Strategies Select", page)
            self.pageTechAnStrategiesLabel.setFixedSize(860, 25)
            self.pageTechAnStrategiesLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pageTechAnStrategiesLabel)
            self.pageTechAnStrategiesWidget = QWidget(page)
            self.pageTechAnStrategiesWidget.setFixedSize(700, 80)
            strategiesGrid = QGridLayout()
            strategiesGrid.setContentsMargins(30, 10, 0, 10)
            self.pageTechAnStrategyCheckBoxACOscillator = QCheckBox("  ACOscillator")
            self.pageTechAnStrategyCheckBoxCCICorrection= QCheckBox("  CCI Correction")
            self.pageTechAnStrategyCheckBoxDMRSIADX     = QCheckBox("  DM RSI ADX")
            self.pageTechAnStrategyCheckBoxMACD         = QCheckBox("  MACD")
            self.pageTechAnStrategyCheckBoxBreakoutsSwing=QCheckBox("  Breakouts Swing")
            self.pageTechAnStrategyCheckBoxOscillator313= QCheckBox("  Oscillator3 13")
            self.pageTechAnStrategyCheckBoxACOscillator.setChecked(False)
            self.pageTechAnStrategyCheckBoxCCICorrection.setChecked(False)
            self.pageTechAnStrategyCheckBoxDMRSIADX.setChecked(False)
            self.pageTechAnStrategyCheckBoxMACD.setChecked(True)
            self.pageTechAnStrategyCheckBoxBreakoutsSwing.setChecked(False)
            self.pageTechAnStrategyCheckBoxOscillator313.setChecked(False)
            strategiesGrid.addWidget(self.pageTechAnStrategyCheckBoxACOscillator, *(1, 1))
            strategiesGrid.addWidget(self.pageTechAnStrategyCheckBoxCCICorrection, *(1, 2))
            strategiesGrid.addWidget(self.pageTechAnStrategyCheckBoxDMRSIADX, *(1, 3))
            strategiesGrid.addWidget(self.pageTechAnStrategyCheckBoxMACD, *(2,1))
            strategiesGrid.addWidget(self.pageTechAnStrategyCheckBoxBreakoutsSwing, *(2,2))
            strategiesGrid.addWidget(self.pageTechAnStrategyCheckBoxOscillator313, *(2,3))
            self.pageTechAnStrategiesWidget.setLayout(strategiesGrid)
            pageMainVerticalBox.addWidget(self.pageTechAnStrategiesWidget)

            # trading time config components
            self.pageTechAnTimeSpanLabel = QLabel("Trading Time Config", page)
            self.pageTechAnTimeSpanLabel.setFixedSize(860, 25)
            self.pageTechAnTimeSpanLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pageTechAnTimeSpanLabel)
            timeVbox = QVBoxLayout()
            timeVbox.setContentsMargins(30, 10, 0, 10)
            startTimeHbox = QHBoxLayout()
            self.pageTechAnStartTimeName = QLabel("Start Time: ", page)
            self.pageTechAnStartTimeName.setFont(self.contentFont)
            self.pageTechAnStartTimeName.setFixedSize(100, 25)
            self.pageTechAnStartTimeName.setStyleSheet(self.itemNameQSS)
            startTimeHbox.addWidget(self.pageTechAnStartTimeName)
            self.pageTechAnStartTimeEdit = QLineEdit("2016-02-10 16:00:00")
            self.pageTechAnStartTimeEdit.setEnabled(False)
            self.pageTechAnStartTimeEdit.setStyleSheet(self.lineEditQSS)
            self.pageTechAnStartTimeEdit.setFixedSize(300, 25)
            startTimeHbox.addWidget(self.pageTechAnStartTimeEdit)
            startTimeHbox.addStretch(1)
            timeVbox.addLayout(startTimeHbox)
            endTimeHbox = QHBoxLayout()
            self.pageTechAnEndTimeName = QLabel("End Time: ", page)
            self.pageTechAnEndTimeName.setFont(self.contentFont)
            self.pageTechAnEndTimeName.setFixedSize(100, 25)
            self.pageTechAnEndTimeName.setStyleSheet(self.itemNameQSS)
            endTimeHbox.addWidget(self.pageTechAnEndTimeName)
            self.pageTechAnEndTimeEdit = QLineEdit("2016-02-26 16:00:00")
            self.pageTechAnEndTimeEdit.setEnabled(False)
            self.pageTechAnEndTimeEdit.setStyleSheet(self.lineEditQSS)
            self.pageTechAnEndTimeEdit.setFixedSize(300, 25)
            endTimeHbox.addWidget(self.pageTechAnEndTimeEdit)
            endTimeHbox.addStretch(1)
            timeVbox.addLayout(endTimeHbox)
            pageMainVerticalBox.addLayout(timeVbox)

            # trading strategies select components
            self.pageTechAnTStrSpanLabel = QLabel("Trading Strategies Select", page)
            self.pageTechAnTStrSpanLabel.setFixedSize(860, 25)
            self.pageTechAnTStrSpanLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pageTechAnTStrSpanLabel)
            self.pageTechAnTradeStrateWidget = QWidget(page)
            self.pageTechAnTradeStrateWidget.setFixedSize(700, 40)
            tradeStratGrid = QGridLayout()
            tradeStratGrid.setContentsMargins(30, 5, 0, 5)
            self.pageTechAnTStrRadioButtonVWAP = QRadioButton("  VWAP")
            self.pageTechAnTStrRadioButtonVWAP.setCheckable(False)
            self.pageTechAnTStrRadioButtonTWAP = QRadioButton("  TWAP")
            self.pageTechAnTStrRadioButtonTWAP.setChecked(True)
            self.pageTechAnTStrRadioButtonNONE = QRadioButton("  NONE")
            tradeStratGrid.addWidget(self.pageTechAnTStrRadioButtonVWAP, *(1, 1))
            tradeStratGrid.addWidget(self.pageTechAnTStrRadioButtonTWAP, *(1, 2))
            tradeStratGrid.addWidget(self.pageTechAnTStrRadioButtonNONE, *(1, 3))
            tradeStratGrid.addWidget(QLabel(), *(1, 4))
            tradeStratGrid.addWidget(QLabel(), *(1, 5))
            self.pageTechAnTradeStrateWidget.setLayout(tradeStratGrid)
            pageMainVerticalBox.addWidget(self.pageTechAnTradeStrateWidget)

            # position management method select components
            self.pageTechAnPManSpanLabel = QLabel("Position Management Method Select", page)
            self.pageTechAnPManSpanLabel.setFixedSize(860, 25)
            self.pageTechAnPManSpanLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pageTechAnPManSpanLabel)
            self.pageTechAnPManageMthdWidget = QWidget(page)
            self.pageTechAnPManageMthdWidget.setFixedSize(700, 40)
            pManageMtdGrid = QGridLayout()
            pManageMtdGrid.setContentsMargins(30, 10, 0, 10)
            self.pageTechAnPMtdRadioButtonFixedFraction = QRadioButton("  Fixed Fraction")
            self.pageTechAnPMtdRadioButtonFixedFraction.setChecked(True)
            self.pageTechAnPMtdRadioButtonMaximDrawDown = QRadioButton("  Max Draw Down")
            pManageMtdGrid.addWidget(self.pageTechAnPMtdRadioButtonFixedFraction, *(1, 1))
            pManageMtdGrid.addWidget(self.pageTechAnPMtdRadioButtonMaximDrawDown, *(1, 2))
            pManageMtdGrid.addWidget(QLabel(), *(1, 3))
            pManageMtdGrid.addWidget(QLabel(), *(1, 4))
            pManageMtdGrid.addWidget(QLabel(), *(1, 5))
            self.pageTechAnPManageMthdWidget.setLayout(pManageMtdGrid)
            pageMainVerticalBox.addWidget(self.pageTechAnPManageMthdWidget)

            space = QWidget()
            space.setFixedSize(0, 0)
            pageMainVerticalBox.addWidget(space)

            self.pageTechAnLaunchButton = QPushButton("Launch")
            self.pageTechAnLaunchButton.setFont(self.contentFont)
            self.pageTechAnLaunchButton.setFixedSize(860, 40)
            self.pageTechAnLaunchButton.setStyleSheet(self.launchWdgtReadyQSS)
            self.pageTechAnLaunchButton.clicked.connect(self.pageTechAnLaunch)
            pageMainVerticalBox.addWidget(self.pageTechAnLaunchButton)

            page.setLayout(pageMainVerticalBox)

            self.pagesStatus[ci] = 1

        page.show()

    def pageTechAnLaunch(self):

        capital      = int("".join(re.split("\$| |,", self.pageTechAnCapitalEdit.text())))
        securityCode = self.pageTechAnSecurityCombo.currentText()

        investmentStrategies = []
        if self.pageTechAnStrategyCheckBoxACOscillator.isChecked()  : investmentStrategies.append("ACOscillator")
        if self.pageTechAnStrategyCheckBoxCCICorrection.isChecked() : investmentStrategies.append("CCI_Correction")
        if self.pageTechAnStrategyCheckBoxDMRSIADX.isChecked()      : investmentStrategies.append("DM_RSI_ADX")
        if self.pageTechAnStrategyCheckBoxMACD.isChecked()          : investmentStrategies.append("MACD")
        if self.pageTechAnStrategyCheckBoxBreakoutsSwing.isChecked(): investmentStrategies.append("breakouts_swing")
        if self.pageTechAnStrategyCheckBoxOscillator313.isChecked() : investmentStrategies.append("oscillator3_13")

        startTime = self.pageTechAnStartTimeEdit.text()
        endTime   = self.pageTechAnEndTimeEdit.text()

        tradeStrategy = None
        if self.pageTechAnTStrRadioButtonVWAP.isChecked()   : tradeStrategy = "VWAP"
        if self.pageTechAnTStrRadioButtonTWAP.isChecked()   : tradeStrategy = "TWAP"
        # if self.pageTechAnTStrRadioButtonPOV.isChecked()    : tradeStrategy = "POV"
        # if self.pageTechAnTStrRadioButtonSimple.isChecked() : tradeStrategy = "Simple"
        if self.pageTechAnTStrRadioButtonNONE.isChecked()   : tradeStrategy = "Default"

        positionManagement = None
        if self.pageTechAnPMtdRadioButtonFixedFraction.isChecked()  : positionManagement = "FixedFraction"
        if self.pageTechAnPMtdRadioButtonMaximDrawDown.isChecked()  : positionManagement = "MaximumDrawDown"

        thread.start_new_thread(self.ATM.launchTechnicalAnalysis, (capital, securityCode, investmentStrategies, startTime, endTime, tradeStrategy, positionManagement))

    def pageTechAnLaunchProcess(self):
        self.pageTechAnLaunchButton.setStyleSheet(self.launchWdgtProcesQSS)
        self.pageTechAnLaunchButton.setText("Processing")

    def pageTechAnLaunchFinish(self):
        self.pageTechAnLaunchButton.setStyleSheet(self.launchWdgtReadyQSS)
        self.pageTechAnLaunchButton.setText("Re-Launch")

    # The pair trading page
    def pairTrPage(self):

        # hide all pages to show self page
        for pi in range(0, len(self.pages)):
            self.toolButtons[pi].setStyleSheet(self.toolButtonHideQSS)
            self.pages[pi].hide()

        print "in pair trading page"
        ci = 1
        page = self.pages[ci]
        self.toolButtons[ci].setStyleSheet(self.toolButtonFocusQSS)

        if self.pagesStatus[ci] == 0:
            self.pagePairTrConfigWidget = QWidget(page)
            self.pagePairTrConfigWidget.setFixedSize(860, 700)

            pageMainVerticalBox = QVBoxLayout()
            pageMainVerticalBox.setContentsMargins(0, 5, 0, 0)

            self.pagePairTrTitleLabel = QLabel("Pair Trading")
            self.pagePairTrTitleLabel.setFixedSize(860, 25)
            self.pagePairTrTitleLabel.setStyleSheet(self.pageTitleQSS)
            pageMainVerticalBox.addWidget(self.pagePairTrTitleLabel)

            self.pagePairTrCapitalLabel = QLabel("Capital Config", page)
            self.pagePairTrCapitalLabel.setFixedSize(860, 25)
            self.pagePairTrCapitalLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pagePairTrCapitalLabel)
            capitalHbox = QHBoxLayout()
            capitalHbox.setContentsMargins(30, 10, 0, 10)
            self.pagePairTrCapitalInputLabel = QLabel("Capital: ", page)
            self.pagePairTrCapitalInputLabel.setFont(self.contentFont)
            self.pagePairTrCapitalInputLabel.setFixedSize(100, 25)
            self.pagePairTrCapitalInputLabel.setStyleSheet(self.itemNameQSS)
            capitalHbox.addWidget(self.pagePairTrCapitalInputLabel)
            self.pagePairTrCapitalEdit = QLineEdit("$ 100,000,000")
            self.pagePairTrCapitalEdit.setStyleSheet(self.lineEditQSS)
            self.pagePairTrCapitalEdit.setFixedSize(300, 25)
            self.pagePairTrCapitalEdit.setEnabled(False)
            capitalHbox.addWidget(self.pagePairTrCapitalEdit)
            capitalHbox.addStretch(1)
            pageMainVerticalBox.addLayout(capitalHbox)

            self.pagePairTrSecurityLabel = QLabel("Security Select", page)
            self.pagePairTrSecurityLabel.setFixedSize(860, 25)
            self.pagePairTrSecurityLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pagePairTrSecurityLabel)
            securityHbox = QHBoxLayout()
            securityHbox.setContentsMargins(30, 10, 0, 10)
            self.pagePairTrSecurityCode = QLabel("Security Basket: ", page)
            self.pagePairTrSecurityCode.setFont(self.contentFont)
            self.pagePairTrSecurityCode.setFixedSize(100, 25)
            self.pagePairTrSecurityCode.setStyleSheet(self.itemNameQSS)
            securityHbox.addWidget(self.pagePairTrSecurityCode)
            self.pagePairTrSecurities = QTextEdit(page)
            self.pagePairTrSecurities.setEnabled(False)
            self.pagePairTrSecurities.setFixedSize(600, 148)
            securities = ""
            for item in self.ATM.data.getAssetList("./dataManager/data/hsi_stocks"): securities += item + '   '
            self.pagePairTrSecurities.setText(securities)
            securityHbox.addWidget(self.pagePairTrSecurities)
            securityHbox.addStretch(1)
            pageMainVerticalBox.addLayout(securityHbox)

            self.pagePairTrTimeSpanLabel = QLabel("Trading Time Config", page)
            self.pagePairTrTimeSpanLabel.setFixedSize(860, 25)
            self.pagePairTrTimeSpanLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pagePairTrTimeSpanLabel)
            timeVbox = QVBoxLayout()
            timeVbox.setContentsMargins(30, 10, 0, 10)
            startTimeHbox = QHBoxLayout()
            self.pagePairTrStartTimeName = QLabel("Start Time: ", page)
            self.pagePairTrStartTimeName.setFont(self.contentFont)
            self.pagePairTrStartTimeName.setFixedSize(100, 25)
            self.pagePairTrStartTimeName.setStyleSheet(self.itemNameQSS)
            startTimeHbox.addWidget(self.pagePairTrStartTimeName)
            self.pagePairTrStartTimeEdit = QLineEdit("2016-02-10 16:00:00")
            self.pagePairTrStartTimeEdit.setEnabled(False)
            self.pagePairTrStartTimeEdit.setStyleSheet(self.lineEditQSS)
            self.pagePairTrStartTimeEdit.setFixedSize(300, 25)
            startTimeHbox.addWidget(self.pagePairTrStartTimeEdit)
            startTimeHbox.addStretch(1)
            timeVbox.addLayout(startTimeHbox)
            endTimeHbox = QHBoxLayout()
            self.pagePairTrEndTimeName = QLabel("End Time: ", page)
            self.pagePairTrEndTimeName.setFont(self.contentFont)
            self.pagePairTrEndTimeName.setFixedSize(100, 25)
            self.pagePairTrEndTimeName.setStyleSheet(self.itemNameQSS)
            endTimeHbox.addWidget(self.pagePairTrEndTimeName)
            self.pagePairTrEndTimeEdit = QLineEdit("2016-02-26 16:00:00")
            self.pagePairTrEndTimeEdit.setEnabled(False)
            self.pagePairTrEndTimeEdit.setStyleSheet(self.lineEditQSS)
            self.pagePairTrEndTimeEdit.setFixedSize(300, 25)
            endTimeHbox.addWidget(self.pagePairTrEndTimeEdit)
            endTimeHbox.addStretch(1)
            timeVbox.addLayout(endTimeHbox)
            pageMainVerticalBox.addLayout(timeVbox)

            self.pagePairTrTStrSpanLabel = QLabel("Trading Strategies Select", page)
            self.pagePairTrTStrSpanLabel.setFixedSize(860, 25)
            self.pagePairTrTStrSpanLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pagePairTrTStrSpanLabel)
            self.pagePairTrTradeStrateWidget = QWidget(page)
            self.pagePairTrTradeStrateWidget.setFixedSize(700, 40)
            tradeStratGrid = QGridLayout()
            tradeStratGrid.setContentsMargins(30, 5, 0, 5)
            self.pagePairTrTStrRadioButtonVWAP = QRadioButton("  VWAP")
            self.pagePairTrTStrRadioButtonVWAP.setCheckable(False)
            self.pagePairTrTStrRadioButtonTWAP = QRadioButton("  TWAP")
            self.pagePairTrTStrRadioButtonTWAP.setChecked(True)
            self.pagePairTrTStrRadioButtonNONE = QRadioButton("  NONE")
            tradeStratGrid.addWidget(self.pagePairTrTStrRadioButtonVWAP, *(1, 1))
            tradeStratGrid.addWidget(self.pagePairTrTStrRadioButtonTWAP, *(1, 2))
            tradeStratGrid.addWidget(self.pagePairTrTStrRadioButtonNONE, *(1, 3))
            tradeStratGrid.addWidget(QLabel(), *(1, 4))
            tradeStratGrid.addWidget(QLabel(), *(1, 5))
            self.pagePairTrTradeStrateWidget.setLayout(tradeStratGrid)
            pageMainVerticalBox.addWidget(self.pagePairTrTradeStrateWidget)

            self.pagePairTrPManSpanLabel = QLabel("Position Management Method Select", page)
            self.pagePairTrPManSpanLabel.setFixedSize(860, 25)
            self.pagePairTrPManSpanLabel.setStyleSheet(self.pageSubTitleQSS)
            pageMainVerticalBox.addWidget(self.pagePairTrPManSpanLabel)
            self.pagePairTrPManageMthdWidget = QWidget(page)
            self.pagePairTrPManageMthdWidget.setFixedSize(700, 40)
            pManageMtdGrid = QGridLayout()
            pManageMtdGrid.setContentsMargins(30, 10, 0, 10)
            self.pagePairTrPMtdRadioButtonFixedFraction = QRadioButton("  Fixed Fraction")
            self.pagePairTrPMtdRadioButtonFixedFraction.setChecked(True)
            self.pagePairTrPMtdRadioButtonMaximDrawDown = QRadioButton("  Max Draw Down")
            pManageMtdGrid.addWidget(self.pagePairTrPMtdRadioButtonFixedFraction, *(1, 1))
            pManageMtdGrid.addWidget(self.pagePairTrPMtdRadioButtonMaximDrawDown, *(1, 2))
            pManageMtdGrid.addWidget(QLabel(), *(1, 3))
            pManageMtdGrid.addWidget(QLabel(), *(1, 4))
            pManageMtdGrid.addWidget(QLabel(), *(1, 5))
            self.pagePairTrPManageMthdWidget.setLayout(pManageMtdGrid)
            pageMainVerticalBox.addWidget(self.pagePairTrPManageMthdWidget)

            space = QWidget()
            space.setFixedSize(0, 0)
            pageMainVerticalBox.addWidget(space)

            self.pagePairTrLaunchButton = QPushButton("Launch")
            self.pagePairTrLaunchButton.setFont(self.contentFont)
            self.pagePairTrLaunchButton.setFixedSize(860, 40)
            self.pagePairTrLaunchButton.setStyleSheet(self.launchWdgtReadyQSS)
            self.pagePairTrLaunchButton.clicked.connect(self.pagePairTrdLaunch)
            pageMainVerticalBox.addWidget(self.pagePairTrLaunchButton)

            page.setLayout(pageMainVerticalBox)

            self.pagesStatus[ci] = 1

        page.show()

    def pagePairTrdLaunch(self):

        capital = int("".join(re.split("\$| |,", self.pagePairTrCapitalEdit.text())))

        investmentStrategies = ["pairstrading", ]

        startTime = self.pagePairTrStartTimeEdit.text()
        endTime = self.pagePairTrEndTimeEdit.text()

        tradeStrategy = None
        if self.pagePairTrTStrRadioButtonVWAP.isChecked(): tradeStrategy = "VWAP"
        if self.pagePairTrTStrRadioButtonTWAP.isChecked(): tradeStrategy = "TWAP"
        if self.pagePairTrTStrRadioButtonNONE.isChecked(): tradeStrategy = "Default"

        positionManagement = None
        if self.pagePairTrPMtdRadioButtonFixedFraction.isChecked(): positionManagement = "FixedFraction"
        if self.pagePairTrPMtdRadioButtonMaximDrawDown.isChecked(): positionManagement = "MaximumDrawDown"

        thread.start_new_thread(self.ATM.launchPairTradingAnalysis, (capital, investmentStrategies, startTime, endTime, tradeStrategy, positionManagement))

    def pagePairTrdLaunchProcess(self):
        self.pagePairTrLaunchButton.setStyleSheet(self.launchWdgtProcesQSS)
        self.pagePairTrLaunchButton.setText("Processing")

    def pagePairTrdLaunchFinish(self):
        self.pagePairTrLaunchButton.setStyleSheet(self.launchWdgtReadyQSS)
        self.pagePairTrLaunchButton.setText("Re-Launch")

    def atoTrdPage(self):

        for pi in range(0,len(self.pages)):
            self.toolButtons[pi].setStyleSheet(self.toolButtonHideQSS)
            self.pages[pi].hide()

        print "in monitor page"
        ci = 2
        page = self.pages[ci]
        self.toolButtons[ci].setStyleSheet(self.toolButtonFocusQSS)

        if self.pagesStatus[ci] == 0:

            if not page.layout() == None:
                while page.layout().count() > 0:
                    page.layout().takeAt(0).widget().setParent(None)

            if page.layout() == None:
                self.pageAutoTrdPageMainVerticalBox = QVBoxLayout()
                self.pageAutoTrdPageMainVerticalBox.setContentsMargins(0, 5, 0, 0)
                page.setLayout(self.pageAutoTrdPageMainVerticalBox)

            self.pageAutoTrdTitleLabel = QLabel("Monitor", page)
            self.pageAutoTrdTitleLabel.setFixedSize(860, 25)
            self.pageAutoTrdTitleLabel.setStyleSheet(self.pageTitleQSS)
            self.pageAutoTrdPageMainVerticalBox.addWidget(self.pageAutoTrdTitleLabel)

            pnlReport = self.ATM.report
            if not len(self.ATM.strategies.strategiesPool.keys()) == 0:
                self.pageAtoTrdPageScroll = QScrollArea(page)
                self.pageAtoTrdPageScroll.setWidgetResizable(True)
                self.pageAtoTrdPageScroll.setBackgroundRole(QPalette.NoRole)
                self.pageAtoTrdPageScroll.setStyleSheet("background: transparent")
                self.pageAtoTrdPageScroll.setFixedSize(860, 635)
                self.pageAtoTrdScrollContentsWidget = QWidget(page)
                scrollContentVBox = QVBoxLayout()
                scrollContentVBox.setAlignment(Qt.AlignTop)
                scrollContentVBox.setContentsMargins(0, 0, 0, 0)

                self.pageAtoTrdSignalPlotLabel = QLabel("Signals Plots", page)
                self.pageAtoTrdSignalPlotLabel.setFixedSize(860, 25)
                self.pageAtoTrdSignalPlotLabel.setStyleSheet(self.pageSubTitleQSS)
                scrollContentVBox.addWidget(self.pageAtoTrdSignalPlotLabel)

                path = "./strategies/image/"
                for file in os.listdir(path):
                    if file.endswith(".png") and file.split('.')[0] in self.ATM.strategies.strategiesPool.keys():
                        pageAtoTrdSignalPlotStrategyLabel = QLabel(file.split('.')[0], page)
                        pageAtoTrdSignalPlotStrategyLabel.setFixedSize(860, 25)
                        pageAtoTrdSignalPlotStrategyLabel.setStyleSheet(self.pageSubSubTitleQSS)
                        scrollContentVBox.addWidget(pageAtoTrdSignalPlotStrategyLabel)

                        widget = QWidget()
                        widget.setFixedHeight(300)
                        hbox = QHBoxLayout()
                        hbox.setContentsMargins(0, 0, 0, 0)
                        hbox.setAlignment(Qt.AlignCenter)
                        lbl = QLabel()
                        pixmap = QPixmap(path + file)
                        scaled_pixmap = pixmap.scaled(860, 330, Qt.KeepAspectRatio)
                        lbl.setPixmap(scaled_pixmap)
                        hbox.addWidget(lbl)
                        widget.setLayout(hbox)
                        scrollContentVBox.addWidget(widget)

                self.pageAtoTrdAllSignalsLabel = QLabel("All Signals", page)
                self.pageAtoTrdAllSignalsLabel.setFixedSize(860, 25)
                self.pageAtoTrdAllSignalsLabel.setStyleSheet(self.pageSubTitleQSS)
                scrollContentVBox.addWidget(self.pageAtoTrdAllSignalsLabel)

                self.pageAtoTrdAllSignalsTitle = QWidget(page)
                self.pageAtoTrdAllSignalsTitle.setFixedSize(860, 25)
                self.pageAtoTrdAllSignalsTitle.setStyleSheet(self.pageSubSubTitleQSS)
                titlesHBox = QHBoxLayout()
                titlesHBox.setContentsMargins(10, 0, 20, 0)
                titlesHBox.addWidget(QLabel("Code"))
                titlesHBox.addWidget(QLabel("Time"))
                titlesHBox.addWidget(QLabel("Action"))
                titlesHBox.addWidget(QLabel("Qnt"))
                titlesHBox.addWidget(QLabel("Price"))
                titlesHBox.addWidget(QLabel("Volumn"))
                titlesHBox.addWidget(QLabel("Strategy"))
                self.pageAtoTrdAllSignalsTitle.setLayout(titlesHBox)
                scrollContentVBox.addWidget(self.pageAtoTrdAllSignalsTitle)

                signals = self.ATM.strategies.signals
                if not len(signals) == 0:
                    for i in xrange(len(signals)):
                        widget = QWidget(page)
                        widget.setFixedHeight(15)
                        widget.setStyleSheet("color:#ffffff")
                        signalHBox = QHBoxLayout()
                        signalHBox.setContentsMargins(20, 0, 10, 0)
                        signalHBox.addWidget(QLabel(signals.ix[i]["Code"]))
                        signalHBox.addWidget(QLabel(str(signals.ix[i]["Time"])))
                        signalHBox.addWidget(QLabel(signals.ix[i]["Action"]))
                        signalHBox.addWidget(QLabel(str(signals.ix[i]["Qnt"])))
                        signalHBox.addWidget(QLabel(str(signals.ix[i]["Price"])))
                        signalHBox.addWidget(QLabel(str(signals.ix[i]["Volume"])))
                        signalHBox.addWidget(QLabel(signals.ix[i]["Strategy"]))
                        widget.setLayout(signalHBox)
                        scrollContentVBox.addWidget(widget)

                else:
                    widget = QLabel("No Data.")
                    widget.setFixedSize(860, 550)
                    widget.setStyleSheet(self.noDataLabelQSS)
                    widget.setAlignment(Qt.AlignCenter)
                    scrollContentVBox.addWidget(widget)

                self.pageAtoTrdScrollContentsWidget.setLayout(scrollContentVBox)
                self.pageAtoTrdPageScroll.setWidget(self.pageAtoTrdScrollContentsWidget)
                self.pageAutoTrdPageMainVerticalBox.addWidget(self.pageAtoTrdPageScroll)

            else:
                widget = QLabel("No Data.")
                widget.setFixedSize(860, 550)
                widget.setStyleSheet(self.noDataLabelQSS)
                widget.setAlignment(Qt.AlignCenter)
                self.pageAutoTrdPageMainVerticalBox.addWidget(widget)

            self.pagesStatus[ci] = 1

        page.show()

    def trdPnlPage(self):

        for pi in range(0,len(self.pages)):
            self.toolButtons[pi].setStyleSheet(self.toolButtonHideQSS)
            self.pages[pi].hide()

        print "in profit and loss report page"
        ci = 3
        page = self.pages[ci]
        self.toolButtons[ci].setStyleSheet(self.toolButtonFocusQSS)

        if self.pagesStatus[ci] == 0:

            if not page.layout() == None:
                while page.layout().count() > 0:
                    page.layout().takeAt(0).widget().setParent(None)

            if page.layout() == None:
                self.pageTrdPnlPageMainVerticalBox = QVBoxLayout()
                self.pageTrdPnlPageMainVerticalBox.setContentsMargins(0, 5, 0, 0)
                page.setLayout(self.pageTrdPnlPageMainVerticalBox)

            self.pageTrdHisTitleLabel = QLabel("Profit And Loss Report", page)
            self.pageTrdHisTitleLabel.setFixedSize(860, 25)
            self.pageTrdHisTitleLabel.setStyleSheet(self.pageTitleQSS)
            self.pageTrdPnlPageMainVerticalBox.addWidget(self.pageTrdHisTitleLabel)

            pnlReport = self.ATM.report
            if not len(pnlReport) == 0:

                self.pageTrdHisBookTitles = QWidget(page)
                self.pageTrdHisBookTitles.setFixedSize(860, 25)
                self.pageTrdHisBookTitles.setStyleSheet(self.pageSubTitleQSS)
                titlesHBox = QHBoxLayout()
                titlesHBox.setContentsMargins(10, 0, 20, 0)
                strategy = QLabel("Strategy")
                titlesHBox.addWidget(QLabel("Strategy"))
                titlesHBox.addWidget(QLabel("Realized PnL"))
                titlesHBox.addWidget(QLabel("Return"))
                areturn = QLabel("Annual Return")
                areturn.setFixedWidth(130)
                titlesHBox.addWidget(areturn)
                titlesHBox.addWidget(QLabel("Volatility"))
                titlesHBox.addWidget(QLabel("Sharpe Ratio"))
                mdd = QLabel("Maximum Draw Down")
                mdd.setFixedWidth(155)
                titlesHBox.addWidget(mdd)
                self.pageTrdHisBookTitles.setLayout(titlesHBox)
                self.pageTrdPnlPageMainVerticalBox.addWidget(self.pageTrdHisBookTitles)


                self.pageTrdHisPageScroll = QScrollArea(page)
                self.pageTrdHisPageScroll.setWidgetResizable(True)
                self.pageTrdHisPageScroll.setBackgroundRole(QPalette.NoRole)
                self.pageTrdHisPageScroll.setStyleSheet("background: transparent")
                self.pageTrdHisPageScroll.setFixedSize(860, 600)
                self.pageTrdHisScrollContentsWidget = QWidget(page)
                scrollContentVBox = QVBoxLayout()
                scrollContentVBox.setAlignment(Qt.AlignTop)
                scrollContentVBox.setContentsMargins(0, 0, 0, 0)
                for i in xrange(0, len(pnlReport)):
                    widget = QWidget()
                    widget.setFixedHeight(15)
                    if pnlReport.ix[i]["realized PnL"] > 0: widget.setStyleSheet("color:#fa2020")
                    if pnlReport.ix[i]["realized PnL"] < 0: widget.setStyleSheet("color:#27AE60")
                    hbox   = QHBoxLayout()
                    hbox.setContentsMargins(20, 0, 10, 0)
                    strategy = QLabel(pnlReport.ix[i]["Strategy"])
                    strategy.setFixedWidth(100)
                    hbox.addWidget(strategy)
                    hbox.addWidget(QLabel(str("{0:.2f}".format(pnlReport.ix[i]["realized PnL"]))))
                    hbox.addWidget(QLabel(str("{0:.4f}".format(pnlReport.ix[i]["Return"]))))
                    areturn = QLabel(str("{0:.4f}".format(pnlReport.ix[i]["Annualized Return"])))
                    # hbox.addWidget(QLabel(str("{0:.2f}".format(tradeHistory.ix[i]["QntPer"] * 100))))
                    areturn.setFixedWidth(130)
                    hbox.addWidget(areturn)
                    hbox.addWidget(QLabel(str("{0:.4f}".format(pnlReport.ix[i]["Volatility"]))))
                    hbox.addWidget(QLabel(str("{0:.4f}".format(pnlReport.ix[i]["Sharpe Ratio"]))))
                    mdd = QLabel(str("{0:.6f}".format(pnlReport.ix[i]["MDD"])))
                    mdd.setFixedWidth(155)
                    hbox.addWidget(mdd)
                    widget.setLayout(hbox)
                    scrollContentVBox.addWidget(widget)
                self.pageTrdHisScrollContentsWidget.setLayout(scrollContentVBox)
                self.pageTrdHisPageScroll.setWidget(self.pageTrdHisScrollContentsWidget)
                self.pageTrdPnlPageMainVerticalBox.addWidget(self.pageTrdHisPageScroll)

            else:
                widget = QLabel("No Data.")
                widget.setFixedSize(860, 550)
                widget.setStyleSheet(self.noDataLabelQSS)
                widget.setAlignment(Qt.AlignCenter)
                self.pageTrdPnlPageMainVerticalBox.addWidget(widget)

            self.pagesStatus[ci] = 1

        page.show()

    def trdHisPage(self):

        for pi in range(0,len(self.pages)):
            self.toolButtons[pi].setStyleSheet(self.toolButtonHideQSS)
            self.pages[pi].hide()

        print "in trade history page"
        ci = 4
        page = self.pages[ci]
        self.toolButtons[ci].setStyleSheet(self.toolButtonFocusQSS)

        if self.pagesStatus[ci] == 0:

            if not page.layout() == None:
                while page.layout().count() > 0:
                    page.layout().takeAt(0).widget().setParent(None)

            if page.layout() == None:
                self.pageTrdHisPageMainVerticalBox = QVBoxLayout()
                self.pageTrdHisPageMainVerticalBox.setContentsMargins(0, 5, 0, 0)
                page.setLayout(self.pageTrdHisPageMainVerticalBox)

            self.pageTrdHisTitleLabel = QLabel("Trade History", page)
            self.pageTrdHisTitleLabel.setFixedSize(860, 25)
            self.pageTrdHisTitleLabel.setStyleSheet(self.pageTitleQSS)
            self.pageTrdHisPageMainVerticalBox.addWidget(self.pageTrdHisTitleLabel)

            tradeHistory = self.ATM.account.queryTradeHistory()

            if not len(tradeHistory) == 0:
                self.pageTrdHisBookTitles = QWidget(page)
                self.pageTrdHisBookTitles.setFixedSize(860, 25)
                self.pageTrdHisBookTitles.setStyleSheet(self.pageSubTitleQSS)
                titlesHBox = QHBoxLayout()
                titlesHBox.setContentsMargins(10, 0, 20, 0)
                code = QLabel("Code")
                code.setFixedWidth(100)
                titlesHBox.addWidget(code)
                time = QLabel("Time")
                time.setFixedWidth(145)
                titlesHBox.addWidget(time)
                titlesHBox.addWidget(QLabel("Action"))
                qnt = QLabel("Qnt")
                qnt.setFixedWidth(50)
                titlesHBox.addWidget(qnt)
                titlesHBox.addWidget(QLabel("Occupy"))
                titlesHBox.addWidget(QLabel("Price"))
                titlesHBox.addWidget(QLabel("PnL"))
                titlesHBox.addWidget(QLabel("Equity"))
                strategy = QLabel("Strategy")
                strategy.setFixedWidth(100)
                titlesHBox.addWidget(strategy)
                self.pageTrdHisBookTitles.setLayout(titlesHBox)
                self.pageTrdHisPageMainVerticalBox.addWidget(self.pageTrdHisBookTitles)

                self.pageTrdHisPageScroll = QScrollArea(page)
                self.pageTrdHisPageScroll.setWidgetResizable(True)
                self.pageTrdHisPageScroll.setBackgroundRole(QPalette.NoRole)
                self.pageTrdHisPageScroll.setStyleSheet("background: transparent")
                self.pageTrdHisPageScroll.setFixedSize(860, 600)
                self.pageTrdHisScrollContentsWidget = QWidget(page)
                scrollContentVBox = QVBoxLayout()
                scrollContentVBox.setContentsMargins(0, 0, 0, 0)
                scrollContentVBox.setAlignment(Qt.AlignTop)
                for i in xrange(0, len(tradeHistory)):
                    widget = QWidget()
                    widget.setFixedHeight(15)
                    if tradeHistory.ix[i]["Action"] == "Short" : widget.setStyleSheet("color:#27AE60")
                    if tradeHistory.ix[i]["Action"] == "SellToCover"  : widget.setStyleSheet("color:#27AE60")
                    if tradeHistory.ix[i]["Action"] == "Long" : widget.setStyleSheet("color:#fa2020")
                    if tradeHistory.ix[i]["Action"] == "BuyToCover" : widget.setStyleSheet("color:#fa2020")
                    hbox   = QHBoxLayout()
                    hbox.setContentsMargins(20, 0, 10, 0)
                    code = QLabel(str(tradeHistory.ix[i]["Code"])); code.setFixedWidth(100); hbox.addWidget(code);
                    time = QLabel(str(tradeHistory.ix[i]["Time"])); time.setFixedWidth(145); hbox.addWidget(time);
                    hbox.addWidget(QLabel(tradeHistory.ix[i]["Action"]))
                    qnt = QLabel(str(tradeHistory.ix[i]["Qnt"])); qnt.setFixedWidth(50); hbox.addWidget(qnt);
                    hbox.addWidget(QLabel(str("{0:.2f}".format(tradeHistory.ix[i]["QntPer"] * 100))+"%"))
                    hbox.addWidget(QLabel(str(round(tradeHistory.ix[i]["Price"]))))
                    pnl = QLabel()
                    if not tradeHistory.ix[i]["PnL"] == "": pnl = QLabel(str(round(float(tradeHistory.ix[i]["PnL"]))));
                    hbox.addWidget(pnl)
                    hbox.addWidget(QLabel(str(round(tradeHistory.ix[i]["Equity"]))))
                    strategy = QLabel(tradeHistory.ix[i]["Strategy"]); strategy.setFixedWidth(100); hbox.addWidget(strategy);
                    widget.setLayout(hbox)
                    scrollContentVBox.addWidget(widget)
                self.pageTrdHisScrollContentsWidget.setLayout(scrollContentVBox)
                self.pageTrdHisPageScroll.setWidget(self.pageTrdHisScrollContentsWidget)
                self.pageTrdHisPageMainVerticalBox.addWidget(self.pageTrdHisPageScroll)

            else:
                widget = QLabel("No Data.")
                widget.setFixedSize(860, 550)
                widget.setStyleSheet(self.noDataLabelQSS)
                widget.setAlignment(Qt.AlignCenter)
                self.pageTrdHisPageMainVerticalBox.addWidget(widget)

            self.pagesStatus[ci] = 1

        page.show()

    def setStyle(self):

        self.setStyleSheet(
            "QToolBar {" +
                "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #203138, stop: 1.0 #000000);" +
                "border-right: 1px solid #065279;" +
                "padding: 5px}" +
            "QToolBar > QToolButton {" +
                "color: #ffffff;" +
                "font-family:'ArialRegular';" +
                "font-size: 14px}" +
            "QToolBar > QToolButton:hover {" +
                "background: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 #ffcb06, stop: 1.0 #ff9c28);" +
                "border-radius:3px}" +
            "QLabel {" +
                "font-family:'ArialRegular';" +
                "padding: 10px;}" +
            "QPushButton {" +
                "height: 20px}" +
            "QComboBox {" +
                "border-radius: 1px; " +
                "border-top-right-radius:11px;" +
                "border-bottom-right-radius:11px;" +
                "font-family:'ArialRegular'}" +
            "QComboBox::drop-down {" +
                "width:15px;" +
                "background-color: #ff9c28;" +
                "border-top-right-radius:10px;" +
                "border-bottom-right-radius:10px;}" +
            "QCheckBox {" +
                "color: #ffffff;" +
                "font-family:'ArialRegular'}" +
            "QCheckBox::indicator {" +
                "background-color:#ffffff;" +
                "border-radius: 1px}" +
            "QCheckBox::indicator:checked {" +
                "background-color:#ff9c28}" +
            "QLineEdit {" +
                "background:#ff9c28;" +
                "border-radius:1px}" +
            "QLineEdit:focus {" +
                "border-radius:1px;}" +
            "QRadioButton {color: #ffffff}" +
            "QScrollArea {border:0px; background:transparent}" +
            "QTextEdit {padding-left: 5px; border: 0px; font-family: 'ArialRegular'; font-weight:20; font-size:14px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ec2f4b, stop: 1.0 #85030f);}"
        )

        self.mainBoardQSS       = "padding:0px; background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #203138, stop: 1.0 #000000);"
        self.pagesQSS           = "background:none; padding: 0px"
        self.pageTitleQSS       = "padding-left:5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ec2f4b, stop: 1.0 #85030f); color: #ffffff; font-family: 'ArialRegular'; font-weight:20; font-size: 16px"
        self.pageSubTitleQSS    = "padding-left:5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #495d76, stop: 1.0 #1f4e7c); color: #dddddd; font-family: 'ArialRegular'; font-weight:20; font-size: 14px"
        self.pageSubSubTitleQSS = "padding-left:5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #646464, stop: 1.0 #838683); color: #dddddd; font-family: 'ArialRegular'; font-weight:20; font-size: 14px"
        self.toolButtonHideQSS  = "background:none; font-size: 14px; font-family:'ArialRegular'"
        self.toolButtonFocusQSS = "background:qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 #ffcb06, stop: 1.0 #ff9c28);border-radius:3px; color:#000000"
        self.itemNameQSS        = "color: #ffffff; font-family: 'ArialRegular'"
        self.comboQSS           = "padding-left:5px;background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eeeeee, stop: 1.0 #dddddd);"
        self.lineEditQSS        = "background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eeeeee, stop: 1.0 #dddddd);border: 0px; padding-left:5px; font-family:'ArialRegular'; font-weight:20; font-size: 14px"
        self.launchWdgtReadyQSS = "background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #004900, stop: 1.0 #033502);border: 0px; color:#ffffff"
        self.launchWdgtProcesQSS= "background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #006602, stop: 1.0 #007b03);border: 0px; color:#ffffff"
        self.tableTitleQSS      = "padding-left:5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #495d76, stop: 1.0 #1f4e7c); color: #dddddd; font-family: 'ArialRegular'; font-weight:20; font-size: 14px"
        self.noDataLabelQSS     = "color: #ffffff; font-family: ArialRegular; font-weight: 20; font-size: 14px"
        self.pageTitleFont  = QFont('ArialRegular')
        self.titleFont      = QFont('ArialRegular')
        self.contentFont    = QFont('ArialRegular')

        self.pageTitleColor = "#ffffff"
        self.titleColor     = "#ffffff"
        self.contentColor   = "#ffffff"