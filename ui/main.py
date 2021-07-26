# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os

from PyQt5 import QtCore, QtWidgets

import SshAuvLib
import blackBox


class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):
        self.W = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.operatorTree = QtWidgets.QListWidget(self.centralwidget)
        self.operatorTree.setGeometry(QtCore.QRect(10, 40, 351, 501))
        self.operatorTree.setObjectName("operatorTree")
        self.apparatusTree = QtWidgets.QListWidget(self.centralwidget)
        self.apparatusTree.setGeometry(QtCore.QRect(450, 40, 341, 501))
        self.apparatusTree.setObjectName("apparatusTree")
        self.syncAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.syncAllButton.setGeometry(QtCore.QRect(370, 190, 75, 23))
        self.syncAllButton.setObjectName("syncAllButton")
        self.syncSelectButton = QtWidgets.QPushButton(self.centralwidget)
        self.syncSelectButton.setGeometry(QtCore.QRect(370, 220, 75, 23))
        self.syncSelectButton.setObjectName("syncSelectButton")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(370, 250, 75, 41))
        self.deleteButton.setObjectName("deleteButton")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setObjectName("backButton")
        self.backButton.setGeometry(QtCore.QRect(10, 520, 75, 23))
        self.loginText = QtWidgets.QLineEdit(self.centralwidget)
        self.loginText.setGeometry(QtCore.QRect(10, 10, 113, 20))
        self.loginText.setObjectName("loginText")
        self.portText = QtWidgets.QLineEdit(self.centralwidget)
        self.portText.setGeometry(QtCore.QRect(480, 10, 41, 20))
        self.portText.setObjectName("portText")
        self.passwordText = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordText.setGeometry(QtCore.QRect(140, 10, 113, 20))
        self.passwordText.setObjectName("passwordText")
        self.ipText = QtWidgets.QLineEdit(self.centralwidget)
        self.ipText.setGeometry(QtCore.QRect(270, 10, 191, 20))
        self.ipText.setInputMask("")
        self.ipText.setObjectName("ipText")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(540, 10, 101, 23))
        self.connectButton.setObjectName("connectButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.syncAllButton.setText(_translate("MainWindow", "<<<"))
        self.syncSelectButton.setText(_translate("MainWindow", "<"))
        self.deleteButton.setText(_translate("MainWindow", "Удалить\n"
                                                           "выделенное"))
        self.backButton.setText(_translate("MainWindow", "Назад"))
        self.loginText.setText(_translate("MainWindow", "kosta"))
        self.portText.setText(_translate("MainWindow", "22"))
        self.passwordText.setText(_translate("MainWindow", "89140273987Qq"))
        self.ipText.setText(_translate("MainWindow", "localhost"))
        self.connectButton.setText(_translate("MainWindow", "Подключиться"))

    def add_functions(self):
        self.connectButton.clicked.connect(
            lambda: self.connect_session(self.ipText.text(), self.loginText.text(), self.passwordText.text(),
                                         self.portText.text()))
        self.syncSelectButton.clicked.connect(
            lambda: self.select_file_transport(self.apparatusTree.currentItem().text()))
        self.syncAllButton.clicked.connect(lambda: self.all_file_transport())
        self.deleteButton.clicked.connect(lambda: self.delete(self.apparatusTree.currentItem().text()))
        self.operatorTree.doubleClicked.connect(
            lambda: self.double_click(self.operatorTree.currentItem().text(), self.W))
        self.backButton.clicked.connect(self.back)

    def connect_session(self, host, username, secret, port):
        self.SSHSession = SshAuvLib.SshAuvSession(host.split(' '), username, secret, int(port))
        self.SSHSession.connection()
        self.SSHSession.open_sftp_sessions()
        self.SSHSession.change_work_path('C:\\Users\\kosta\\Downloads\\TestClient')
        self.SSHSession.change_sftp_work_path('C:\\Users\\kosta\\Downloads\\TestServer')
        self._update_tree()

    def select_file_transport(self, file):
        self.SSHSession.download_and_extract_files([file])
        self._update_tree()

    def all_file_transport(self):
        self.SSHSession.download_and_extract_files(self.SSHSession.get_sftp_file_list())
        self._update_tree()

    def delete(self, file):
        self.SSHSession.delete_files([file])
        self._update_tree()

    def back(self):
        if os.getcwd() != 'C:\\Users\\kosta\\Downloads\\TestClient':
            self.SSHSession.change_work_path('..')
        self._update_tree()

    def double_click(self, file, W):
        if os.path.isdir(file):
            self.SSHSession.change_work_path(file)
        if file == 'blackbox.txt':
            logs = blackBox.get_logs('blackbox.txt')
            msgbox = QtWidgets.QMessageBox(W)
            logs_str = ''
            if len(logs) == 0:
                logs_str = 'Ошибок нет'
            for log in logs:
                logs_str += '['
                logs_str += 'WARNING' if log[0] == 'w' else 'ERROR'
                logs_str += ' '
                logs_str += log[1]
                logs_str += ' '
                logs_str += log[2]
                logs_str += '] '
                logs_str += log[3]
                logs_str += '\n'
            msgbox.setText(logs_str)
            msgbox.setWindowTitle('ERROR!!!!1111!!!!11!')
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.show()
        self._update_tree()

    def _update_tree(self):
        self.operatorTree.clear()
        self.apparatusTree.clear()
        self.operatorTree.addItems(self.SSHSession.get_file_list())
        self.apparatusTree.addItems(self.SSHSession.get_sftp_file_list())
