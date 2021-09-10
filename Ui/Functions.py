"""此文件包含关于借书，还书的一些条件判断函数和一些界面组件显示控制函数"""
import datetime
import time
import SQL_SELECT


def Pushtton_Huanshu(main_ui, count):  # 还书按钮控制的显示
    if count == 0:
        main_ui.book1.setVisible(False)
        main_ui.book2.setVisible(False)
        main_ui.book3.setVisible(False)
        main_ui.book4.setVisible(False)
        main_ui.book5.setVisible(False)
        main_ui.book6.setVisible(False)
    if count == 1:
        main_ui.book1.setVisible(True)
        main_ui.book2.setVisible(False)
        main_ui.book3.setVisible(False)
        main_ui.book4.setVisible(False)
        main_ui.book5.setVisible(False)
        main_ui.book6.setVisible(False)
    if count == 2:
        main_ui.book1.setVisible(True)
        main_ui.book2.setVisible(True)
        main_ui.book3.setVisible(False)
        main_ui.book4.setVisible(False)
        main_ui.book5.setVisible(False)
        main_ui.book6.setVisible(False)
    if count == 3:
        main_ui.book1.setVisible(True)
        main_ui.book2.setVisible(True)
        main_ui.book3.setVisible(True)
        main_ui.book4.setVisible(False)
        main_ui.book5.setVisible(False)
        main_ui.book6.setVisible(False)
    if count == 4:
        main_ui.book1.setVisible(True)
        main_ui.book2.setVisible(True)
        main_ui.book3.setVisible(True)
        main_ui.book4.setVisible(True)
        main_ui.book5.setVisible(False)
        main_ui.book6.setVisible(False)
    if count == 5:
        main_ui.book1.setVisible(True)
        main_ui.book2.setVisible(True)
        main_ui.book3.setVisible(True)
        main_ui.book4.setVisible(True)
        main_ui.book5.setVisible(True)
        main_ui.book6.setVisible(False)
    if count==6:
        main_ui.book1.setVisible(True)
        main_ui.book2.setVisible(True)
        main_ui.book3.setVisible(True)
        main_ui.book4.setVisible(True)
        main_ui.book5.setVisible(True)
        main_ui.book6.setVisible(True)


def TheFineCalculation(day2):  # 计算超期罚金，day2为应还日期
    i = datetime.datetime.now()  # 获取当前日期
    day1 = str(i.year) + '-' + str(i.month).zfill(2) + '-' + str(i.day).zfill(2)  # 得到还书当天的日期
    time_array1 = time.strptime(day1, "%Y-%m-%d")
    timestamp_day1 = int(time.mktime(time_array1))
    time_array2 = time.strptime(day2, "%Y-%m-%d")
    timestamp_day2 = int(time.mktime(time_array2))
    result = (timestamp_day1 - timestamp_day2) // 60 // 60 // 24
    if int(result) <= 0:  # 没有超出日期
        return 0
    Fine = 0.02 * int(result)
    return Fine  # 返回罚金


def TheTotalFine(result):  # 计算总罚金数
    count = 0
    for i in range(len(result)):
        if result[i][6] is None:  # 是未归还图书
            count += TheFineCalculation(result[i][4])
    return count


def UpdateTheFine(result):
    result = list(result)
    for i in range(len(result)):
        if result[i][6] is None:  # 是未归还图书
            fine = TheFineCalculation(result[i][4])
            if fine > 0:
                SQL_SELECT.UpdateFine(result[i][1], result[i][0], result[i][7], fine)
