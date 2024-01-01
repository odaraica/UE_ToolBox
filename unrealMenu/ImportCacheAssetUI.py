from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys



class ImportCacheAssetUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


    def setupUi(self, ImportCacheAssetUI):
        ImportCacheAssetUI.setObjectName("ImportCacheAssetUI")
        ImportCacheAssetUI.resize(980, 416)
        ImportCacheAssetUI.setStyleSheet("background-color:rgb(50,50,50);border-color:rgb(50,50,50);")
        self.getShotData_Button = QPushButton(ImportCacheAssetUI)
        self.getShotData_Button.setGeometry(QRect(890, 30, 75, 23))
        self.getShotData_Button.setObjectName("getShotData_Button")
        self.getShotData_Button.setStyleSheet("background-color:rgb(80,80,80);")
        self.epsode_comboBox = QComboBox(ImportCacheAssetUI)
        self.epsode_comboBox.setGeometry(QRect(260, 70, 231, 21))
        self.epsode_comboBox.setObjectName("epsode_comboBox")
        self.epsode_comboBox.setStyleSheet("background-color:rgb(100,100,100);")
        self.project_comboBox = QComboBox(ImportCacheAssetUI)
        self.project_comboBox.setGeometry(QRect(50, 70, 191, 21))
        self.project_comboBox.setObjectName("project_comboBox")
        self.project_comboBox.setStyleSheet("background-color:rgb(100,100,100);")
        self.episode_label = QLabel(ImportCacheAssetUI)
        self.episode_label.setGeometry(QRect(260, 50, 54, 12))
        self.episode_label.setObjectName("episode_label")
        self.shot_label = QLabel(ImportCacheAssetUI)
        self.shot_label.setGeometry(QRect(510, 50, 54, 12))
        self.shot_label.setObjectName("shot_label")
        self.importCacheAsset_Button = QPushButton(ImportCacheAssetUI)
        self.importCacheAsset_Button.setGeometry(QRect(890, 70, 75, 23))
        self.importCacheAsset_Button.setObjectName("importCacheAsset_Button")
        self.importCacheAsset_Button.setStyleSheet("background-color:rgb(80,80,80);")
        self.listWidget = QListWidget(ImportCacheAssetUI)
        self.listWidget.setGeometry(QRect(510, 70, 361, 301))
        self.listWidget.setObjectName("listWidget")
        item = QListWidgetItem()
        self.listWidget.addItem(item)
        item = QListWidgetItem()
        self.listWidget.addItem(item)
        self.project_label = QLabel(ImportCacheAssetUI)
        self.project_label.setGeometry(QRect(50, 50, 54, 12))
        self.project_label.setObjectName("project_label")

        self.retranslateUi(ImportCacheAssetUI)
        QMetaObject.connectSlotsByName(ImportCacheAssetUI)

        self.getShotData_Button.clicked.connect(self.getShotDataEvent)
        self.importCacheAsset_Button.clicked.connect(self.importCacheAssetEvent)

    def retranslateUi(self, ImportCacheAssetUI):
        _translate = QCoreApplication.translate
        ImportCacheAssetUI.setWindowTitle(_translate("ImportCacheAssetUI", "导入动画缓存文件插件"))
        self.getShotData_Button.setText(_translate("ImportCacheAssetUI", "获取项目信息"))
        self.episode_label.setText(_translate("ImportCacheAssetUI", "集数"))
        self.shot_label.setText(_translate("ImportCacheAssetUI", "镜头"))
        self.importCacheAsset_Button.setText(_translate("ImportCacheAssetUI", "导入缓存文件"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("ImportCacheAssetUI", "PV001_001-003"))
        item = self.listWidget.item(1)
        item.setText(_translate("ImportCacheAssetUI", "PV001_004"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.project_label.setText(_translate("ImportCacheAssetUI", "项目"))

    def getShotDataEvent(self):
        print('getShotData')

    def importCacheAssetEvent(self):
        print('importAnimAsset')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ICAUI = ImportCacheAssetUI()

    ICAUI.show()
    sys.exit(app.exec_())
