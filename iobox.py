#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu, \
    QDialog, QProgressBar, QLabel, QPushButton, QInputDialog


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


class SettingBox(QDialog):
    progressBarSpace: QProgressBar
    labelSpace: QLabel
    pushButtonAccount: QPushButton

    def __init__(self, *args, **kwargs):
        super().__init__(flags=Qt.Qt.WindowStaysOnTopHint, *args, **kwargs)
        self.tray = SysTray(self)
        self.settings = QSettings()
        self.init_ui()

    def init_ui(self):
        loadUi('resource/setting.ui', self)

        self.progressBarSpace.setVisible(False)
        self.labelSpace.setVisible(False)
        self.pushButtonAccount.clicked.connect(self.login)
        self.tray.show()

    def login(self):
        res = QInputDialog(self)

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setOrganizationName('IoNull')
    app.setOrganizationDomain('ionull.com')
    app.setApplicationName('IoBox')
    tray = SettingBox(None)
    sys.exit(app.exec_())

