from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import ImportAnimAsset as IAA


class ImportAnimAssetUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.IAA = IAA.ImportAnimAsset()

    def setupUi(self, ImportAnimAssetUI):
        ImportAnimAssetUI.setObjectName("ImportAnimAssetUI")
        ImportAnimAssetUI.resize(980, 416)
        ImportAnimAssetUI.setStyleSheet("background-color:rgb(50,50,50);border-color:rgb(50,50,50);")
        self.getShotData_Button = QPushButton(ImportAnimAssetUI)
        self.getShotData_Button.setGeometry(QRect(890, 30, 75, 23))
        self.getShotData_Button.setObjectName("getShotData_Button")
        self.getShotData_Button.setStyleSheet("background-color:rgb(80,80,80);")
        self.epsode_comboBox = QComboBox(ImportAnimAssetUI)
        self.epsode_comboBox.setGeometry(QRect(260, 70, 231, 21))
        self.epsode_comboBox.setObjectName("epsode_comboBox")
        self.epsode_comboBox.setStyleSheet("background-color:rgb(100,100,100);")
        self.project_comboBox = QComboBox(ImportAnimAssetUI)
        self.project_comboBox.setGeometry(QRect(50, 70, 191, 21))
        self.project_comboBox.setObjectName("project_comboBox")
        self.project_comboBox.setStyleSheet("background-color:rgb(100,100,100);")
        self.episode_label = QLabel(ImportAnimAssetUI)
        self.episode_label.setGeometry(QRect(260, 50, 54, 12))
        self.episode_label.setObjectName("episode_label")
        self.shot_label = QLabel(ImportAnimAssetUI)
        self.shot_label.setGeometry(QRect(510, 50, 54, 12))
        self.shot_label.setObjectName("shot_label")
        self.importAnimAsset_Button = QPushButton(ImportAnimAssetUI)
        self.importAnimAsset_Button.setGeometry(QRect(890, 70, 75, 23))
        self.importAnimAsset_Button.setObjectName("importAnimAsset_Button")
        self.importAnimAsset_Button.setStyleSheet("background-color:rgb(80,80,80);")
        self.listWidget = QListWidget(ImportAnimAssetUI)
        self.listWidget.setGeometry(QRect(510, 70, 361, 301))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("background-color:rgb(100,100,100);")
        item = QListWidgetItem()
        self.listWidget.addItem(item)
        item = QListWidgetItem()
        self.listWidget.addItem(item)
        self.project_label = QLabel(ImportAnimAssetUI)
        self.project_label.setGeometry(QRect(50, 50, 54, 12))
        self.project_label.setObjectName("project_label")

        self.retranslateUi(ImportAnimAssetUI)
        QMetaObject.connectSlotsByName(ImportAnimAssetUI)

        self.getShotData_Button.clicked.connect(self.getShotDataEvent)
        self.importAnimAsset_Button.clicked.connect(self.importAnimAssetEvent)
        self.project_comboBox.activated.connect(self.comboBox_project_getInfo)
        self.epsode_comboBox.activated.connect(self.comboBox_epsode_getInfo)

    def retranslateUi(self, ImportAnimAssetUI):
        _translate = QCoreApplication.translate
        ImportAnimAssetUI.setWindowTitle(_translate("ImportAnimAssetUI", "导入绑定角色动画插件"))
        self.getShotData_Button.setText(_translate("ImportAnimAssetUI", "获取项目信息"))
        self.episode_label.setText(_translate("ImportAnimAssetUI", "集数"))
        self.shot_label.setText(_translate("ImportAnimAssetUI", "镜头"))
        self.importAnimAsset_Button.setText(_translate("ImportAnimAssetUI", "导入动画文件"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("ImportAnimAssetUI", "PV001_001-003"))
        item = self.listWidget.item(1)
        item.setText(_translate("ImportAnimAssetUI", "PV001_004"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.project_label.setText(_translate("ImportAnimAssetUI", "项目"))

    def getShotDataEvent(self):
        self.IAA.getProjectData()

        self.project_comboBox.clear()
        self.epsode_comboBox.clear()
        self.listWidget.clear()

        if self.IAA.projectList:
            self.project_comboBox.addItems(self.IAA.projectList)
            self.IAA.getEpsodeData(self.IAA.projectList[0])
            if self.IAA.epsodeList:
                for item in self.IAA.epsodeList:  # 1-10
                    self.epsode_comboBox.addItem(item)

    def importAnimAssetEvent(self):
        #*****************************************************
        choose_project = self.project_comboBox.currentText()
        choose_epsode = self.epsode_comboBox.currentText()
        choose_shot_list = []
        choose_shots = self.listWidget.selectedItems()
        if choose_shots:
            for item in choose_shots:
                choose_shot_list.append(item.text())
        else:
            choose_shot_list = self.IAA.shotList

        #***********************debug**************************
        self.IAA.getSkeletonPath()

    def comboBox_project_getInfo(self):
        choose_project = self.project_comboBox.currentText()
        self.epsode_comboBox.clear()
        self.listWidget.clear()
        self.IAA.getEpsodeData(choose_project)
        if self.IAA.epsodeList:
            self.epsode_comboBox.addItems(self.IAA.epsodeList)
            self.IAA.getShotData(choose_project,self.IAA.epsodeList[0])
            if self.IAA.shotList:
                for item in self.IAA.shotList:
                    self.listWidget.addItem(item)


    def comboBox_epsode_getInfo(self):
        choose_project = self.project_comboBox.currentText()
        choose_epsode = self.epsode_comboBox.currentText()
        self.listWidget.clear()

        self.IAA.getShotData(choose_project, choose_epsode)
        if self.IAA.shotList:
            for item in self.IAA.shotList:
                self.listWidget.addItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    IAAUI = ImportAnimAssetUI()

    IAAUI.show()
    sys.exit(app.exec_())