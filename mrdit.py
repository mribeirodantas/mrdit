#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (©) 2014 Marcel Ribeiro Dantas
#
# mribeirodantas at fedoraproject.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import getpass
import datetime
from PyQt4 import QtGui
from subprocess import call

# What time is it?
hour = datetime.datetime.now().time().hour

if hour >= 0 and hour < 12:
    greeting = "Good morning, "
elif hour >= 12 and hour < 18:
    greeting = "Good afternoon, "
else:  # If it is >= 18 and < 0
    greeting = "Good evening, "

# Username
username = str(getpass.getuser())

# Default size of text
textSize = '10'


class MainWindow(QtGui.QMainWindow):

    # Method for creating a new object of this class
    # AKA class constructor
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    # Creating a new file
    def newFile(self):
        self.textEdit.clear()

    # Dialog for choosing a file to open
    def openFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open a document',
                '/home/' + username)
        # If any path was chosen
        if fname != '':
            f = open(fname, 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)

    # Dialog for choosing a path to save your file
    def saveFile(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save document',
                '/home/' + username)
        f = open(fname, 'w')
        filedata = self.textEdit.toPlainText()
        f.write(filedata)
        f.close()

    # The event of quiting the window by clicking on the x at the right top
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u'You may have unsaved con' +
                                                  'tent right now.',
            u"Are you sure you want to leave?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # Method for centering the window at startup
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def incFontSize(self):
        global textSize
        textSize = str(int(textSize) + 1)
        self.textEdit.setStyleSheet('font-size: ' + textSize + 'pt;')

    def decFontSize(self):
        global textSize
        if int(textSize) > 1:
            textSize = str(int(textSize) - 1)
            self.textEdit.setStyleSheet('font-size: ' + textSize + 'pt;')

    def terminal(self):
        call(["gnome-terminal"])

    # Method for starting up the User Interface
    def initUI(self):
        # Status Bar
        self.statusBar().showMessage(u'The free KISS editor that respects you.')

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

        # Defining text size
        self.textEdit.setStyleSheet('font-size: ' + textSize + 'pt;')

        # Menu items

        newFile = QtGui.QAction(QtGui.QIcon('icons/new.png'),
                  '&New document', self)
        newFile.setShortcut('Ctrl+N')
        newFile.setStatusTip('New File')
        newFile.triggered.connect(self.newFile)

        openFile = QtGui.QAction(QtGui.QIcon('icons/open.png'),
                   '&Open a document', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openFile)

        saveFile = QtGui.QAction(QtGui.QIcon('icons/save.png'),
                   '&Save document', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveFile)

        incFont = QtGui.QAction(QtGui.QIcon('icons/decfontsize.png'),
                  '&Increase font size', self)
        incFont.setShortcut('Ctrl+I')
        incFont.setStatusTip('Increase font size')
        incFont.triggered.connect(self.incFontSize)

        decFont = QtGui.QAction(QtGui.QIcon('icons/incfontsize.png'),
                  '&Decrease font size', self)
        decFont.setShortcut('Ctrl+D')
        decFont.setStatusTip('Decrease font size')
        decFont.triggered.connect(self.decFontSize)

        pyInteractive = QtGui.QAction(QtGui.QIcon('icons/terminal.png'),
                        'Open &terminal', self)
        pyInteractive.setShortcut('Ctrl+T')
        pyInteractive.setStatusTip('Open terminal')
        pyInteractive.triggered.connect(self.terminal)

        exitAction = QtGui.QAction(QtGui.QIcon('icons/exit.png'), '&Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(u'Quit the Application')
        exitAction.triggered.connect(self.close)

        # Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFile)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(incFont)
        fileMenu.addAction(decFont)
        fileMenu.addAction(pyInteractive)
        fileMenu.addAction(exitAction)

         # Toolbar
        QtGui.QAction(QtGui.QIcon('open.png'), '', self)
        self.toolbar = self.addToolBar('Editor toolbar')
        self.toolbar.addAction(newFile)
        self.toolbar.addAction(openFile)
        self.toolbar.addAction(saveFile)
        self.toolbar.addAction(incFont)
        self.toolbar.addAction(decFont)
        self.toolbar.addAction(pyInteractive)
        self.toolbar.addAction(exitAction)

        # Size of window
        self.resize(600, 400)
        self.center()

        self.setWindowTitle(greeting + username + "!" + " Welcome to [mrdit]")

        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
