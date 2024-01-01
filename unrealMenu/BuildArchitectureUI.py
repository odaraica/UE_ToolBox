from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import BuildArchitecture as BA





class Build_ArchitectureUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.BA = BA.Build_Architecture()


    def setupUi(self, Build_ArchitectureUI):
        Build_ArchitectureUI.setObjectName("Build_ArchitectureUI")
        Build_ArchitectureUI.resize(1002, 517)
        Build_ArchitectureUI.setStyleSheet("background-color:rgb(50,50,50);border-color:rgb(50,50,50);")
        self.getShotData_Button = QPushButton(Build_ArchitectureUI)
        self.getShotData_Button.setGeometry(QRect(880, 40, 75, 23))
        self.getShotData_Button.setObjectName("getShotData_Button")
        self.getShotData_Button.setStyleSheet("background-color:rgb(80,80,80);")
        self.project_label = QLabel(Build_ArchitectureUI)
        self.project_label.setGeometry(QRect(40, 60, 54, 12))
        self.project_label.setObjectName("project_label")
        self.listWidget = QListWidget(Build_ArchitectureUI)
        self.listWidget.setGeometry(QRect(500, 80, 361, 301))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("background-color:rgb(100,100,100);")
        item = QListWidgetItem()
        self.listWidget.addItem(item)
        item = QListWidgetItem()
        self.listWidget.addItem(item)
        self.project_comboBox = QComboBox(Build_ArchitectureUI)
        self.project_comboBox.setGeometry(QRect(40, 80, 191, 21))
        self.project_comboBox.setObjectName("project_comboBox")
        self.project_comboBox.setStyleSheet("background-color:rgb(100,100,100);")
        self.episode_label = QLabel(Build_ArchitectureUI)
        self.episode_label.setGeometry(QRect(250, 60, 54, 12))
        self.episode_label.setObjectName("episode_label")
        self.epsode_comboBox = QComboBox(Build_ArchitectureUI)
        self.epsode_comboBox.setGeometry(QRect(250, 80, 231, 21))
        self.epsode_comboBox.setObjectName("epsode_comboBox")
        self.epsode_comboBox.setStyleSheet("background-color:rgb(100,100,100);")
        self.shot_label = QLabel(Build_ArchitectureUI)
        self.shot_label.setGeometry(QRect(500, 60, 54, 12))
        self.shot_label.setObjectName("shot_label")
        self.buildFolder_Button = QPushButton(Build_ArchitectureUI)
        self.buildFolder_Button.setGeometry(QRect(880, 80, 75, 23))
        self.buildFolder_Button.setObjectName("buildFolder_Button")
        self.buildFolder_Button.setStyleSheet("background-color:rgb(80,80,80);")

        self.retranslateUi(Build_ArchitectureUI)
        QMetaObject.connectSlotsByName(Build_ArchitectureUI)

        self.getShotData_Button.clicked.connect(self.getShotDataEvent)
        self.buildFolder_Button.clicked.connect(self.buildFolderEvent)
        self.project_comboBox.activated.connect(self.comboBox_project_getInfo)
        self.epsode_comboBox.activated.connect(self.comboBox_epsode_getInfo)

    def retranslateUi(self, Build_ArchitectureUI):
        _translate = QCoreApplication.translate
        Build_ArchitectureUI.setWindowTitle(_translate("Build_ArchitectureUI", "UE工程架构建立插件1.0"))
        self.getShotData_Button.setText(_translate("Build_ArchitectureUI", "获取项目信息"))
        self.project_label.setText(_translate("Build_ArchitectureUI", "项目"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Build_ArchitectureUI", "PV001_001-003"))
        item = self.listWidget.item(1)
        item.setText(_translate("Build_ArchitectureUI", "PV001_004"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.episode_label.setText(_translate("Build_ArchitectureUI", "集数"))
        self.shot_label.setText(_translate("Build_ArchitectureUI", "镜头"))
        self.buildFolder_Button.setText(_translate("Build_ArchitectureUI", "创建ue目录"))

    def getShotDataEvent(self):
        self.BA.getProjectData()

        self.project_comboBox.clear()
        self.epsode_comboBox.clear()
        self.listWidget.clear()

        if self.BA.projectList:
            self.project_comboBox.addItems(self.BA.projectList)
            self.BA.getEpsodeData(self.BA.projectList[0])
            if self.BA.epsodeList:
                for item in self.BA.epsodeList:  # 1-10
                    self.epsode_comboBox.addItem(item)


    def buildFolderEvent(self):
        # **************************************************************************
        choose_project = self.project_comboBox.currentText()
        choose_epsode = self.epsode_comboBox.currentText()
        choose_shot_list = []
        choose_shots = self.listWidget.selectedItems()
        if choose_shots:
            for item in choose_shots:
                choose_shot_list.append(item.text())
        else:
            choose_shot_list = self.BA.shotList
        self.BA.create_folder()
        self.BA.createShotFolderAndSequence(choose_project,choose_epsode,choose_shot_list)
        self.BA.connectSequenceAsset()
        #****************************debug*************************************************
        # self.BA.testBuild()
        #self.BA.testConn()



    def comboBox_project_getInfo(self):
        choose_project = self.project_comboBox.currentText()
        self.epsode_comboBox.clear()
        self.listWidget.clear()

        self.BA.getEpsodeData(choose_project)
        if self.BA.epsodeList:
            self.epsode_comboBox.addItems(self.BA.epsodeList)
            self.BA.getShotData(choose_project,self.BA.epsodeList[0])
            if self.BA.shotList:
                for item in self.BA.shotList:
                    self.listWidget.addItem(item)


    def comboBox_epsode_getInfo(self):
        choose_project = self.project_comboBox.currentText()
        choose_epsode = self.epsode_comboBox.currentText()
        self.listWidget.clear()

        self.BA.getShotData(choose_project, choose_epsode)
        if self.BA.shotList:
            for item in self.BA.shotList:
                self.listWidget.addItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    TBUI = Build_ArchitectureUI()

    TBUI.show()
    sys.exit(app.exec_())
