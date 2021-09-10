"""登录界面"""

import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import Login_rc
from Main import Main_ui
from Admini_Login import Ad_Login,AdL
from SQL_SELECT import db_check_username, db_check_password

app = QApplication(sys.argv)


class MyWindows(Login_rc.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWindows, self).__init__()
        self.setupUi(self)

    def forLogin(self):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if name == "" or password == "":
            reply = QMessageBox.warning(self, "警告", "账号密码不能为空，请输入！")
            return
        if not db_check_username(name):
            if db_check_password(name, password):
                print("登录成功")
                Login_ui.close()
                time.sleep(0.5)
                main_ui.show()
                main_ui.labelsno.setText(name)
            else:
                reply = QtWidgets.QMessageBox.warning(self, "警告", "密码错误!")
        else:
            print("登录失败")
            reply = QtWidgets.QMessageBox.question(self, "警告", "用户名错误!", QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")

    def clearInput(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")

    def OpenAdmini(self):
        AdL.show()


Login_ui = MyWindows()
Login_ui.setWindowTitle("登录")
palette = QPalette()
palette.setBrush(QPalette.Background, QBrush(QPixmap("./images/Login2.jpg")))
Login_ui.setPalette(palette)
main_ui = Main_ui()
palette1 = QPalette()
palette1.setBrush(QPalette.Background, QBrush(QPixmap("./images/main4.jpg")))
main_ui.setPalette(palette1)
main_ui.stackedWidget.setCurrentWidget(main_ui.Welcome_page)
main_ui.label_20.setVisible(False)
main_ui.label_21.setVisible(False)
main_ui.label_41.setVisible(False)
main_ui.lineEdit_5.setVisible(False)
main_ui.lineEdit_6.setVisible(False)
main_ui.lineEdit_13.setVisible(False)
main_ui.pushButton_18.setVisible(False)
main_ui.pushButton_19.setVisible(False)
Login_ui.show()
AdLogin = Ad_Login()
AdLogin.setWindowTitle("管理员登录")
sys.exit(app.exec_())
