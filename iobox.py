#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu, \
    QDialog, QProgressBar, QLabel, QPushButton, QLineEdit


__author__ = 'xiwei'


class SysTray(QSystemTrayIcon):

    """
    sys tray
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # type: SettingBox
        self.menu = QMenu()
        self.icon = QIcon('logo.png')
        self.init_ui()

    def init_menu(self):
        """
        init menu
        """
        self.menu.addAction('设置', self.setting)
        self.menu.addSeparator()
        self.menu.addAction('退出', self.exit)
        self.setIcon(self.icon)
        self.setContextMenu(self.menu)

    def exit(self):
        self.hide()
        app.quit()

    def setting(self):
        """
        open setting box
        :return:
        """
        self.parent.show()

    def alert(self, title: str, content: str):
        self.showMessage(title, content)

    def init_ui(self):
        """
        init ui
        """
        self.init_menu()
        self.show()


class LoginBox(QDialog):
    pushButtonLogin: QPushButton
    pushButtonCancel: QPushButton
    lineEditUsername: QLineEdit
    lineEditPassword: QLineEdit

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, flags=Qt.Qt.WindowStaysOnTopHint, *args, **kwargs)
        loadUi('resource/login.ui', self)
        self.parent = parent  # type: SettingBox

        self.pushButtonCancel.clicked.connect(self.close)
        self.pushButtonLogin.clicked.connect(self.login)
        self.lineEditUsername.setText(self.parent.settings.value('username', ''))
        self.lineEditPassword.setText(self.parent.settings.value('password', ''))

    def login(self):
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        self.parent.settings.setValue('username', username)
        self.parent.settings.setValue('password', password)
        self.parent.check_account()
        self.close()


class SettingBox(QDialog):
    progressBarSpace: QProgressBar
    labelSpace: QLabel
    pushButtonAccount: QPushButton

    def __init__(self, *args, **kwargs):
        super().__init__(flags=Qt.Qt.WindowStaysOnTopHint, *args, **kwargs)
        self.tray = SysTray(self)
        self.settings = QSettings()
        self.init_ui()
        self.check_account()

    def init_ui(self):
        loadUi('resource/setting.ui', self)

        self.pushButtonAccount.clicked.connect(self.login)
        self.tray.show()

    def check_account(self):
        if self.username:
            self.pushButtonAccount.setText(f"注销:{self.username}")
            self.progressBarSpace.setVisible(True)
            self.progressBarSpace.setDisabled(False)
            self.progressBarSpace.setMaximum(50)
            self.progressBarSpace.setValue(13)
            self.labelSpace.setVisible(True)
        else:
            self.pushButtonAccount.setText("登录")
            self.progressBarSpace.setVisible(False)
            self.labelSpace.setVisible(False)
            self.show()

    @property
    def username(self):
        return self.settings.value('username', False)

    def login(self):
        if self.username:
            self.settings.remove('username')
            self.settings.remove('password')
            self.check_account()
        else:
            res = LoginBox(self)
            res.show()

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setOrganizationName('IoNull')
    app.setOrganizationDomain('ionull.com')
    app.setApplicationName('IoBox')
    with open('resource/style.qss', 'r') as style:
        app.setStyleSheet(style.read())
    tray = SettingBox(None)
    sys.exit(app.exec_())

