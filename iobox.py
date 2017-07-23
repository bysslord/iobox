#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu


__author__ = 'xiwei'


class SysTray(QSystemTrayIcon):

    """
    sys tray
    """

    def __init__(self):
        super().__init__()
        self.menu = QMenu()
        self.icon = QIcon('logo.png')
        self.settings = QSettings()
        self.initUI()

    def initMenu(self):
        """
        init menu
        """
        self.menu.addAction('alert', self.test)
        self.menu.addAction('退出', app.quit)
        self.setIcon(self.icon)
        self.setContextMenu(self.menu)

    def test(self):
        self.alert('iobox', 'test')

    def alert(self, title: str, content: str):
        print(title, content)
        self.showMessage(title, content)

    def initUI(self):
        """
        init ui
        """
        self.initMenu()
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setOrganizationName('IoNull')
    app.setOrganizationDomain('ionull.com')
    app.setApplicationName('IoBox')
    tray = SysTray()
    sys.exit(app.exec_())

