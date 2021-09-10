import time

from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox

import Admini_Login_rc
from Administrators import Admini
from SQL_SELECT import AdLogin


class Ad_Login(Admini_Login_rc.Ui_Dialog, QMainWindow):
    def __init__(self):
        super(Ad_Login, self).__init__()
        self.setupUi(self)

    def shut(self):
        AdL.lineEdit.setText("")
        AdL.lineEdit_2.setText("")
        AdL.close()

    def open(self):
        UserName = self.lineEdit.text()
        PassWord = self.lineEdit_2.text()
        if UserName == "" or PassWord == "":
            QMessageBox.warning(self, "警告", "输入不能为空！")
        else:
            result = AdLogin(UserName, PassWord)
            if len(result) == 0:
                QMessageBox.warning(self, "警告", "没有此管理员的记录！")
            elif result[0][0] != PassWord:
                QMessageBox.warning(self, "警告", "密码错误！")
            else:
                AdL.close()
                time.sleep(0.5)
                Ad.show()
                Ad.label_Name.setText(str(result[0][1]))
                self.lineEdit_2.setText("")
                self.lineEdit.setText("")


Ad = Admini()
AdL = Ad_Login()
palette = QPalette()
palette.setBrush(QPalette.Background, QBrush(QPixmap("./images/AD.jpg")))
AdL.setWindowTitle("管理员登录")
Ad.setPalette(palette)
Ad.stackedWidget.setCurrentWidget(Ad.page_5)
Ad.setWindowTitle("图书借阅管理子系统")
