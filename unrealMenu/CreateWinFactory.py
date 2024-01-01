from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import unreal
import sys
import ToolBoxUI as TB




class CreateWin:
    def __init__(self):
        self.exist_windows = {}
        self.opened_windows = []

    # def __QtAppTick__(self,delta_seconds):
    #     for window in self.opened_windows:
    #         window.eventTick(delta_seconds)

    def __QtAppQuit__(self,handle):
        unreal.unregister_slate_post_tick_callback(handle)

    def __QtWindowClose__(self,window=None):
        if window in self.opened_windows:
            self.opened_windows.remove(window)

    def createApp(self):
        unreal_app = QApplication.instance()
        if not unreal_app:
            unreal_app = QApplication(sys.argv)
            # tick_handle = unreal.register_slate_post_tick_callback(self.__QtAppTick__())
            # unreal_app.aboutToQuit.connect(self.__QtAppQuit__(tick_handle))
            self.opened_windows.clear()
            self.exist_windows.clear()

    def createQtWindows(self,window_class=None):
        window = self.exist_windows.get(window_class,None)
        if not window:
            window = window_class()
            self.exist_windows[window_class] = window
            window.aboutToClose = self.__QtWindowClose__
        if window not in self.opened_windows:
            self.opened_windows.append(window)

        window.show()
        window.activateWindow()
        return window

#CW = CreateWin()
# CW.createQtWindows(TB.MyWin)