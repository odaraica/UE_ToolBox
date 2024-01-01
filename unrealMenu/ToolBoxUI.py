import sys
import os


from PySide2.QtWidgets import *
from PySide2.QtCore import *

import BuildArchitectureUI as BAUI
import ImportAnimAssetUI as IAAUI
import ImportCacheAssetUI as ICAUI
import ToolBox as TB



class ToolBoxUI(QWidget):

    def __init__(self):
        super(ToolBoxUI,self).__init__()
        self.TB = TB.ToolBox()
        self.BAUI = BAUI.Build_ArchitectureUI()
        self.IAAUI = IAAUI.ImportAnimAssetUI()
        self.ICAUI = ICAUI.ImportCacheAssetUI()
        self.setObjectName("ToolBoxWin")
        self.setWindowTitle("虚拟影业工具箱1.0")
        self.resize(260, 210)
        self.setStyleSheet("background-color:rgb(50,50,50);border-color:rgb(50,50,50);")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(50, 0, 50, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.BuildArchitecture_Button = QPushButton()
        self.BuildArchitecture_Button.setObjectName("BuildArchitecture_Button")
        self.BuildArchitecture_Button.setText("建立文件架构插件")
        self.BuildArchitecture_Button.setStyleSheet("background-color:rgb(80,80,80)")


        self.verticalLayout.addWidget(self.BuildArchitecture_Button)

        self.importAnim_Button = QPushButton()
        self.importAnim_Button.setObjectName("importAnim_Button")
        self.importAnim_Button.setText("导入绑定角色动画")
        self.importAnim_Button.setStyleSheet("background-color:rgb(80,80,80)")

        self.verticalLayout.addWidget(self.importAnim_Button)

        self.importCache_Button = QPushButton()
        self.importCache_Button.setObjectName("importCache_Button")
        self.importCache_Button.setText("导入动画缓存文件")
        self.importCache_Button.setStyleSheet("background-color:rgb(80,80,80)")

        self.verticalLayout.addWidget(self.importCache_Button)


        self.setLayout(self.verticalLayout)

        self.BuildArchitecture_Button.clicked.connect(self.BuildArchitectureEvent)
        self.importAnim_Button.clicked.connect(self.importAnimEvent)
        self.importCache_Button.clicked.connect(self.importCacheEvent)

    def BuildArchitectureEvent(self):
        if self.BAUI.isVisible():
            pass
        else:
            self.BAUI.show()
    def importAnimEvent(self):
        if self.IAAUI.isVisible():
            pass
        else:
            self.IAAUI.show()
    def importCacheEvent(self):
        if self.ICAUI.isVisible():
            pass
        else:
            self.ICAUI.show()


def execu():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    global TBUI
    TBUI = ToolBoxUI()
    TBUI.show()
    TBUI.activateWindow()










