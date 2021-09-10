"""管理员界面"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QLineEdit, QTableWidgetItem, QHeaderView

import Administrators_rc

from SQL_SELECT import UpdateUsersInformation
from SQL_SELECT import list_of_student
from SQL_SELECT import list_of_student2
from SQL_SELECT import Deleteuser
from SQL_SELECT import InsertIntoBooks
from SQL_SELECT import Select_Part_Book
from SQL_SELECT import SelectALLBook

p = False
re = []


class Admini(Administrators_rc.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Admini, self).__init__()
        self.setupUi(self)
        """
        self.actionce.triggered.connect(self.InsertBook)
        self.actione.triggered.connect(self.FindBookIn)
        self.actiony.triggered.connect(self.UserManagement)
        """

    def __compalte(self):  # 初始化
        global re
        self.setupUi(self)  # 重新初始化窗口，在切换页面时将之前的内容删除
        re = []

    def InsertBook(self):
        self.__compalte()
        self.stackedWidget.setCurrentWidget(self.page)

    def InsertIntoBook(self):
        BNO = self.lineEdit_BNO.text()
        BNA = self.lineEdit_BNA.text()
        BDA = self.lineEdit_BDA.text()
        BPU = self.lineEdit_BPU.text()
        BPL = self.lineEdit_BPL.text()
        BNU = self.lineEdit_BNU.text()
        if BNO == "" or BNA == "" or BDA == "" or BPU == "" or BPL == "" or BNU == "":
            QMessageBox.warning(self, "警告", "输入不能为空！")
        else:
            if InsertIntoBooks(BNO, BNA, BDA, BPU, BPL, BNU):
                QMessageBox.about(self, "提示", "添加成功！")
            else:
                QMessageBox.about(self, "提示", "添加失败！请确认书库中是否有相同图书或你的输入有错")

    def FindBookIn(self):  # 进入查询图书界面
        self.__compalte()
        self.stackedWidget.setCurrentWidget(self.page_2)

    def UserManagement(self):
        self.__compalte()
        self.stackedWidget.setCurrentWidget(self.page_3)

    def UpdateUsersIn(self):  # 进入修改用户信息界面
        global re
        if len(re) == 0:
            QMessageBox.about(self, "提示", "没有用户可以被修改！")
        elif len(re) == 1:
            self.label_SNO1.setText(re[0][0])
            self.label_SNA1.setText(re[0][1])
            self.label_SDE1.setText(re[0][2])
            self.label_SSP1.setText(re[0][3])
            self.label_SUP1.setText(str(re[0][4]))
            self.stackedWidget.setCurrentWidget(self.page_4)
        else:
            if len(re) > 1:
                text, okPressed = QInputDialog.getText(self, "输入", "输入你想要修改的用户的借书证号：", QLineEdit.Normal, "")
                if okPressed :
                    result = list_of_student(text)
                    if text == "":
                        QMessageBox.warning(self, "错误", "输入不能为空！")
                    elif len(result) == 0:
                        QMessageBox.warning(self, "错误", "你输入的借书证号有误！")
                    else:
                        self.label_SNO1.setText(result[0][0])
                        self.label_SNA1.setText(result[0][1])
                        self.label_SDE1.setText(result[0][2])
                        self.label_SSP1.setText(result[0][3])
                        self.label_SUP1.setText(str(result[0][4]))
                        self.stackedWidget.setCurrentWidget(self.page_4)

    def ReturnPage(self):  # 修改用户的返回按钮槽函数
        self.stackedWidget.setCurrentWidget(self.page_3)

    def UpdateIn(self):  # 查找用户
        global p, re
        SNA = self.lineEdit_Name.text()
        SNO = self.lineEdit_SNO.text()
        if SNA == "" and SNO == "":
            QMessageBox.warning(self, "警告", "输入不能为空！")
        else:
            print(SNA)
            if SNA != "" and SNO == "":
                re = list_of_student2(SNA)
            else:
                re = list_of_student(SNO)
            if len(re) == 0:
                QMessageBox.warning(self, "提示", "没有找到此人！")
            else:
                p = True
                print(re)
                row = len(re)
                vol = len(re[0])
                self.tableWidget_2.setRowCount(len(re))
                self.tableWidget_2.setColumnCount(len(re[0]))
                column_name = [
                    '借书证号',
                    '姓名',
                    '系别',
                    '所学专业',
                    '借书上限',
                    '密码',
                ]
                self.tableWidget_2.setHorizontalHeaderLabels(column_name)
                for i in range(row):
                    for j in range(vol):
                        self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(re[i][j])))

    def OpenInputLine1(self):
        text, okPressed = QInputDialog.getText(self, "输入", "姓名", QLineEdit.Normal, "")
        if okPressed and text != '':
            SNO = self.label_SNO1.text()
            p = 1
            if UpdateUsersInformation(p, text, SNO):
                self.label_SNA1.setText(text)
                QMessageBox.about(self, "提示", "修改成功！")
            else:
                QMessageBox.warning(self, "警告", "修改失败")

    def OpenInputLine2(self):
        text, okPressed = QInputDialog.getText(self, "输入", "系", QLineEdit.Normal, "")
        if okPressed and text != '':
            SNO = self.label_SNO1.text()
            p = 2
            if UpdateUsersInformation(p, text, SNO):
                self.label_SDE1.setText(text)
                QMessageBox.about(self, "提示", "修改成功！")
            else:
                QMessageBox.warning(self, "警告", "修改失败")

    def OpenInputLine3(self):
        text, okPressed = QInputDialog.getText(self, "输入", "所学专业", QLineEdit.Normal, "")
        if okPressed and text != '':
            SNO = self.label_SNO1.text()
            p = 3
            if UpdateUsersInformation(p, text, SNO):
                self.label_SSP1.setText(text)
                QMessageBox.about(self, "提示", "修改成功！")
            else:
                QMessageBox.warning(self, "警告", "修改失败")

    def OpenInputLine4(self):
        text, okPressed = QInputDialog.getText(self, "输入", "借书上限", QLineEdit.Normal, "")
        if okPressed and text != '':
            SNO = self.label_SNO1.text()
            p = 4
            if UpdateUsersInformation(p, text, SNO):
                self.label_SUP1.setText(text)
                QMessageBox.about(self, "提示", "修改成功！")
            else:
                QMessageBox.warning(self, "警告", "修改失败")

    def DeleteUser(self):  # 删除用户
        global p, re
        if not p:
            QMessageBox.about(self, "提示", "没有用户可以被删除！")
        else:
            if len(re) == 0:
                QMessageBox.about(self, "提示", "没有用户可以被删除！")
            elif len(re) == 1:
                reply = QMessageBox.question(self, "重要提示", "你将删除此用户，同时会将借阅表的信息一并删除，是否继续？",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    if Deleteuser(self.label_SNO1.text()):
                        QMessageBox.about(self, "提示", "删除成功")
                    else:
                        QMessageBox.about(self, "提示", "删除失败")
                    p = False
            else:
                text, okPressed = QInputDialog.getText(self, "输入", "输入你想要删除的用户的借书证号：", QLineEdit.Normal, "")
                if okPressed:
                    result = list_of_student(text)
                    if text == "":
                        QMessageBox.warning(self, "错误", "输入不能为空！")
                    elif len(result) == 0:
                        QMessageBox.warning(self, "错误", "你输入的借书证号有误！")
                    else:
                        if Deleteuser(text):
                            QMessageBox.about(self, "提示", "删除成功")
                            re = []
                        else:
                            QMessageBox.about(self, "提示", "删除失败")

    def SelectPartBook(self):  # 搜索图书
        BNA = self.lineEdit_BookName.text()
        if BNA == "":
            QMessageBox.warning(self, "警告", "输入不能为空！")
        else:
            result = Select_Part_Book(BNA)
            if len(result) == 0:
                QMessageBox.about(self, "提示", "没有找到此书！")
            else:
                row = len(result)
                vol = len(result[0])
                self.tableWidget.setRowCount(row)
                self.tableWidget.setColumnCount(5)
                column_name = [
                    '图书编号',
                    '图书名称',
                    '图书总量',
                    '当前库存',
                    '已借出量',
                ]
                self.tableWidget.setHorizontalHeaderLabels(column_name)
                self.tableWidget.horizontalHeader().resizeSection(1, 160)
                for i in range(row):
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(result[i][0])))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(result[i][1])))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(result[i][5])))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(str(result[i][6])))
                    self.tableWidget.setItem(i, 4, QTableWidgetItem(str(int(result[i][5]) - int(result[i][6]))))

    def SelectAllBook(self):
        result, row, vol = SelectALLBook()
        column_name = [
            '图书编号',
            '图书名称',
            '图书总量',
            '当前库存',
            '已借出量',
        ]
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(column_name)
        self.tableWidget.horizontalHeader().resizeSection(1, 160)
        for i in range(row):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(result[i][0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(result[i][1])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(result[i][5])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(result[i][6])))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(int(result[i][5]) - int(result[i][6]))))
