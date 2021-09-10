"""用户界面"""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLineEdit, QInputDialog

import main_rc
from SQL_SELECT import list_of_student
from SQL_SELECT import SelectALLBook
from SQL_SELECT import SelectBorrowInformation
from SQL_SELECT import SelectBorrowInformation2  # 选出未归还的图书
from SQL_SELECT import Select_Part_Book
from SQL_SELECT import Borrow_Book
from SQL_SELECT import check_Borrow
from Functions import Pushtton_Huanshu
from SQL_SELECT import ReturnBooks
from SQL_SELECT import ReturnBooks2
from Functions import TheFineCalculation
from Functions import TheTotalFine
from Functions import UpdateTheFine
from SQL_SELECT import GetPassword
from SQL_SELECT import UpdatePassword  # 更新密码
from SQL_SELECT import Renewthebook

app = QtWidgets.QApplication(sys.argv)
Fine = 0


class Main_ui(main_rc.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Main_ui, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("图书管理子系统")

    def Relogin(self):  # 退出程序
        QCoreApplication.instance().quit()

    def __compalte(self):  # 初始化
        self.textEdit_detail.clear()  # 清楚输入框的内容

    def ShowInformation(self):
        # 显示控件
        user = self.labelsno.text()
        relsut = list_of_student(user)
        self.label_name.setText(relsut[0][0])
        self.label_dept.setText(relsut[0][1])
        self.label_ssp.setText(relsut[0][2])
        self.label_count.setText(relsut[0][3])
        self.label_sno.setText(relsut[0][4])
        print(relsut)

    def showPersonInformation(self):  # 显示个人信息及修改信息
        self.stackedWidget.setCurrentWidget(self.page)
        user = self.labelsno.text()
        relsut = list_of_student(user)
        self.label_name.setText(relsut[0][1])
        self.label_dept.setText(relsut[0][2])
        self.label_ssp.setText(relsut[0][3])
        self.label_count.setText(str(relsut[0][4]))
        self.label_sno.setText(relsut[0][0])
        print(relsut)

    def showBorrowInformation(self):  # 显示自身借阅信息
        self.stackedWidget.setCurrentWidget(self.page_2)
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())
        print(result)
        count = row
        print(count)
        UpdateTheFine(result)  # 更新每本书的罚金信息
        if count == 0:  # 没有借阅信息，即没有借书情况
            self.tableWidget_2.setVisible(False)
            self.label_BookCount.setVisible(False)
            self.label_BookCount2.setVisible(False)
            self.label_15.setVisible(False)
            self.label_16.setVisible(False)
            self.label_17.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.pushButton_9.setVisible(False)
        else:  # 有借阅信息
            self.label_13.setVisible(False)
            self.tableWidget_2.setVisible(True)
            self.tableWidget_2.setColumnCount(vol - 2)
            self.tableWidget_2.setRowCount(count)
            column_name = [
                '图书编号',
                '图书名称',
                '借书日期',
                '应还日期',
                '罚金(元)',
                '流水号',
            ]
            self.label_BookCount.setText(str(count))  # 显示已借阅书本数
            self.label_BookCount2.setText(str(6 - count))  # 剩余可借阅书本数
            self.tableWidget_2.setHorizontalHeaderLabels(column_name)
            for i in range(count):
                k = 0
                for j in range(vol):
                    if j == 1 or j == 6:
                        continue
                    self.tableWidget_2.setItem(i, k, QTableWidgetItem(str(result[i][j])))
                    k += 1

    def ReFresh1(self):
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())
        UpdateTheFine(result)  # 更新每本书的罚金信息
        self.tableWidget_2.setVisible(True)
        print("刷新")
        print(row)
        if row != 0:
            self.tableWidget_2.setColumnCount(vol - 2)
            self.tableWidget_2.setRowCount(row)
            column_name = [
                '图书编号',
                '图书名称',
                '借书日期',
                '应还日期',
                '罚金(元)',
                '流水号',
            ]
            self.label_BookCount.setText(str(row))  # 显示已借阅书本数
            self.label_BookCount2.setText(str(6 - row))  # 剩余可借阅书本数
            self.tableWidget_2.setHorizontalHeaderLabels(column_name)
            for i in range(row):
                k = 0
                for j in range(vol):
                    if j == 1 or j == 6:
                        continue
                    self.tableWidget_2.setItem(i, k, QTableWidgetItem(str(result[i][j])))
                    k += 1

    def BorrowBook(self):  # 完成借书操作
        BookName = self.lineEdit_3.text()
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())
        Fine = TheTotalFine(result)
        if BookName == "":
            QtWidgets.QMessageBox.warning(self, "提示", "输入不能为空！")
        else:
            if Fine != 0:
                QMessageBox.warning(self, "警告", "你当前有%.2f元的罚金未缴清，暂时无法借书！" % Fine)
            else:
                if row >= 6:
                    QMessageBox.warning(self, "警告", "你已经超过借书上限！")
                else:
                    SNO = self.labelsno.text()
                    result = Select_Part_Book(BookName)
                    if len(result) != 1:
                        QtWidgets.QMessageBox.warning(self, "提示", "请输入正确的书名！")
                    else:
                        BNO = result[0][0]
                        if check_Borrow(BNO, SNO) is True:  # 检查是否已经在借阅中
                            Borrow_Book(BNO, SNO, BookName)
                            QtWidgets.QMessageBox.about(self, "提示", "借阅成功")
                        else:
                            QtWidgets.QMessageBox.warning(self, "警告", "你已经借阅了此图书！")

    def showpage3(self):
        self.stackedWidget.setCurrentWidget(self.page_3)

    def ReturnTheBook(self):  # 还书界面
        self.stackedWidget.setCurrentWidget(self.page_4)
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())
        UpdateTheFine(result)
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())
        Fine = TheTotalFine(result)
        count = row
        if count == 0:
            self.tableWidget_4.setVisible(False)
            self.book1.setVisible(False)
            self.book2.setVisible(False)
            self.book3.setVisible(False)
            self.book4.setVisible(False)
            self.book5.setVisible(False)
            self.book6.setVisible(False)
            self.lable33.setVisible(False)
        else:
            self.tableWidget_4.setVisible(True)
            self.label_22.setVisible(False)
            self.tableWidget_4.setRowCount(count)
            self.tableWidget_4.setColumnCount(vol - 2)
            column_name = [
                '图书编号',
                '图书名称',
                '借书日期',
                '应还日期',
                '罚金(元)',
                '流水号',
            ]
            self.tableWidget_4.setHorizontalHeaderLabels(column_name)
            k = 0
            for i in range(row):
                m = 0
                if result[i][6] is None:
                    for j in range(vol):
                        if j == 1 or j == 6:
                            continue
                        self.tableWidget_4.setItem(k, m, QTableWidgetItem(str(result[i][j])))
                        m += 1
                    k += 1
            Pushtton_Huanshu(self, count)
            if Fine > 0:
                self.lable33.setText("你当期有超期罚金信息，暂时无法还书！请缴清罚金后还书！")
                self.book1.setVisible(False)
                self.book2.setVisible(False)
                self.book3.setVisible(False)
                self.book4.setVisible(False)
                self.book5.setVisible(False)
                self.book6.setVisible(False)

    def ReFresh2(self):
        self.tableWidget_4.setColumnCount(0)
        self.tableWidget_4.setRowCount(0)
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())
        UpdateTheFine(result)  # 更新每本书的罚金信息
        Fine = TheTotalFine(result)
        count = row
        if count == 0:
            self.tableWidget_4.setVisible(False)
            self.book1.setVisible(False)
            self.book2.setVisible(False)
            self.book3.setVisible(False)
            self.book4.setVisible(False)
            self.book5.setVisible(False)
            self.book6.setVisible(False)
            self.lable33.setVisible(False)
        else:
            self.tableWidget_4.setVisible(True)
            self.label_22.setVisible(False)
            self.tableWidget_4.setRowCount(count)
            self.tableWidget_4.setColumnCount(vol - 2)
            column_name = [
                '图书编号',
                '图书名称',
                '借书日期',
                '应还日期',
                '罚金(元)',
                '流水号',
            ]
            self.tableWidget_4.setHorizontalHeaderLabels(column_name)
            k = 0
            for i in range(row):
                m = 0
                if result[i][6] is None:
                    for j in range(vol):
                        if j == 1 or j == 6:
                            continue
                        self.tableWidget_4.setItem(k, m, QTableWidgetItem(str(result[i][j])))
                        m += 1
                    k += 1
            Pushtton_Huanshu(self, count)
            if Fine > 0:
                self.lable33.setText("你当期有超期罚金信息，暂时无法还书！请缴清罚金后还书！")
                self.book1.setVisible(False)
                self.book2.setVisible(False)
                self.book3.setVisible(False)
                self.book4.setVisible(False)
                self.book5.setVisible(False)
                self.book6.setVisible(False)

    def ReturnBook1(self):  # 还书按钮1

        self.ReturnTheBook()
        SNO = self.labelsno.text()
        p = 1
        b = ReturnBooks(p, SNO)
        if b:
            QMessageBox.about(self, "提示", "还书成功")
        else:
            QMessageBox.about(self, "提示", "还书失败！")
        self.ReturnTheBook()

    def ReturnBook2(self):  # 还书按钮2
        self.ReturnTheBook()
        SNO = self.labelsno.text()
        p = 2
        b = ReturnBooks(p, SNO)
        if b:
            QMessageBox.about(self, "提示", "还书成功")
        else:
            QMessageBox.about(self, "提示", "还书失败！")
        self.ReturnTheBook()

    def ReturnBook3(self):  # 还书按钮3
        self.ReturnTheBook()
        SNO = self.labelsno.text()
        p = 3
        b = ReturnBooks(p, SNO)
        if b:
            QMessageBox.about(self, "提示", "还书成功")
        else:
            QMessageBox.about(self, "提示", "还书失败！")
        self.ReturnTheBook()

    def ReturnBook4(self):  # 还书按钮4
        self.ReturnTheBook()
        SNO = self.labelsno.text()
        p = 4
        b = ReturnBooks(p, SNO)
        if b:
            QMessageBox.about(self, "提示", "还书成功")
        else:
            QMessageBox.about(self, "提示", "还书失败！")
        self.ReturnTheBook()

    def ReturnBook5(self):  # 还书按钮5
        self.ReturnTheBook()
        SNO = self.labelsno.text()
        p = 5
        b = ReturnBooks(p, SNO)
        if b:
            QMessageBox.about(self, "提示", "还书成功")
        else:
            QMessageBox.about(self, "提示", "还书失败！")
        self.ReturnTheBook()

    def ReturnBook6(self):  # 还书按钮6
        self.ReturnTheBook()
        SNO = self.labelsno.text()
        p = 6
        b = ReturnBooks(p, SNO)
        if b:
            QMessageBox.about(self, "提示", "还书成功")
        else:
            QMessageBox.about(self, "提示", "还书失败！")
        self.ReturnTheBook()

    def Select_Book(self):  # 搜索指定图书
        bookname = self.lineEdit.text()
        result = Select_Part_Book(bookname)
        if len(result) == 0:
            QtWidgets.QMessageBox.warning(self, "提示", "没有找到这本书！")
        else:
            row = len(result)
            vol = len(result[0])
            self.tableWidget_3.setColumnCount(vol - 1)
            self.tableWidget_3.setRowCount(row)
            column_name = [
                '图书编号',
                '图书名称',
                '出版日期',
                '出版社',
                '图书存放地点',
                '当前库存',
            ]
            self.tableWidget_3.setHorizontalHeaderLabels(column_name)
            for i in range(row):
                for j in range(vol):
                    if j == vol - 2:
                        self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(result[i][j + 1])))
                    else:
                        self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def ShowHistory(self):  # 显示借阅历史
        self.stackedWidget.setCurrentWidget(self.ShowBorrowHistory)
        result, row, vol = SelectBorrowInformation(self.labelsno.text())
        count = 0
        for i in range(row):
            if not result[i][6] is None:
                count += 1
        self.tableWidget.setRowCount(count)
        self.tableWidget.setColumnCount(vol)
        column_name = [
            '图书编号',
            '借书证号',
            '图书名称',
            '借书日期',
            '应还日期',
            '罚金(元)',
            '还书日期',
            '流水号',
        ]
        self.tableWidget.setHorizontalHeaderLabels(column_name)
        k = 0
        for i in range(row):
            if not result[i][6] is None:
                for j in range(vol):
                    self.tableWidget.setItem(k, j, QTableWidgetItem(str(result[i][j])))
                k += 1

    def selectallbook(self):  # 搜索全部图书
        result, row, vol = SelectALLBook()
        for i in range(len(result)):
            print(result[i][:])
        self.tableWidget_3.setColumnCount(vol - 1)
        self.tableWidget_3.setRowCount(row)
        column_name = [
            '图书编号',
            '图书名称',
            '出版日期',
            '出版社',
            '图书存放地点',
            '当前库存',
        ]
        self.tableWidget_3.setHorizontalHeaderLabels(column_name)  # 打印图表
        for i in range(row):
            for j in range(vol):
                if j == vol - 2:
                    self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(result[i][j + 1])))
                else:
                    self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def UpdatePassword(self):  # 打开修改密码的界面
        self.label_20.setVisible(True)
        self.label_21.setVisible(True)
        self.label_41.setVisible(True)
        self.lineEdit_5.setVisible(True)
        self.lineEdit_6.setVisible(True)
        self.lineEdit_13.setVisible(True)
        self.pushButton_18.setVisible(True)
        self.pushButton_19.setVisible(True)

    def ShutPassword(self):  # 关闭修改密码的界面
        self.label_20.setVisible(False)
        self.label_21.setVisible(False)
        self.label_41.setVisible(False)
        self.lineEdit_5.setVisible(False)
        self.lineEdit_6.setVisible(False)
        self.lineEdit_13.setVisible(False)
        self.pushButton_18.setVisible(False)
        self.pushButton_19.setVisible(False)
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_13.setText("")

    def NewPassword(self):  # 修改密码的具体实现
        OldPassword, p = GetPassword(self.labelsno.text())
        password = self.lineEdit_5.text()
        password1 = self.lineEdit_6.text()
        password2 = self.lineEdit_13.text()
        if password1 == "" or password2 == "" or password == "":
            QMessageBox.warning(self, "警告", "输入不能为空！")
        else:
            if not p:
                QMessageBox.warning(self, "错误", "系统错误")
            else:
                if OldPassword is None:
                    if password1 != password2:
                        QMessageBox.warning(self, "错误", "输入的两次新密码不一致！")
                    else:
                        if UpdatePassword(self.labelsno.text(), password1):
                            QMessageBox.about(self, "提示", "修改成功！")
                        else:
                            QMessageBox.about(self, "提示", "修改失败!")
                else:
                    if OldPassword != password:
                        QMessageBox.warning(self, "错误", "请输入正确的旧密码！")
                    else:
                        if password1 != password2:
                            QMessageBox.warning(self, "错误", "输入的两次新密码不一致！")
                        else:
                            if UpdatePassword(self.labelsno.text(), password1):
                                QMessageBox.about(self, "提示", "修改成功！")
                            else:
                                QMessageBox.about(self, "提示", "修改失败!")

    def RenewTheBook(self):  # 规定，续借图书相当于先归还图书后重新借阅，所有有流水号，借阅历史里可以查询到
        BNO = self.lineEdit_4.text()
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())  # 获得未归还的图书列表
        k = 0
        for i in range(len(result)):
            if BNO == result[i][0]:
                break
            k += 1
        if k >= len(result) or BNO == "":
            QMessageBox.warning(self, "错误", "请输入正确的图书编号！")
        else:
            if TheTotalFine(result) != 0:
                QMessageBox.warning(self, "警告", "你当前有%.2f元的超期罚款，请缴清罚款再续借图书！" % TheTotalFine(result))
            else:
                if Renewthebook(self.labelsno.text(), BNO, result):
                    QMessageBox.about(self, "提示", "续借成功！")
                else:
                    QMessageBox.about(self, "提示", "续借失败！")

    def SubmitTheFine(self):
        result, row, vol = SelectBorrowInformation2(self.labelsno.text())  # 获得未归还的图书列表
        fine = TheTotalFine(result)
        if fine == 0:
            QMessageBox.about(self, "提示", "你当前没有超期罚款信息！")
        else:
            reply = QMessageBox.question(self, "提交", "你当前有%.2f元的罚款信息，如果你提交罚款后相应的图书也将还书，是否提交？" % fine,
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                for i in range(len(result)):
                    if result[i][0] != 0:
                        ReturnBooks2(i + 1, result)
                QMessageBox.about(self, "提示", "提交成功！")


# QApplication相当于main函数，也就是整个程序（很多文件）的主入口函数。对于GUI程序必须至少有一个这样的实例来让程序运行。
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_ui = Main_ui()
    main_ui.stackedWidget.setCurrentWidget(main_ui.Welcome_page)
    main_ui.show()
    sys.exit(app.exec_())
