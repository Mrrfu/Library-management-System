import pymssql
import datetime

from PyQt5.QtWidgets import QMessageBox

conn = pymssql.connect(host='localhost', server='LAPTOP-M6B6KHM8\SQLEXPRESS', port='49268', user='sa',
                       password='1033190322',
                       database='BMS')  # 连接数据库 ，port为端口号
cur = conn.cursor()


def db_check_username(username):  # 检查是否有此用户
    sql = "select SNO from Student where SNO = '%s'" % username
    cur.execute(sql)
    result = cur.fetchall()
    if len(result) == 0:
        return True  # 没有找到用户
    else:
        return False


def db_check_password(username, pw_input):  # 检查密码密码
    sql = "select Password from Student where SNO = '%s'" % username
    try:
        cur.execute(sql)
    except Exception as e:
        print("SQL 语句执行错误")
        return False
    else:
        pw_existed = cur.fetchall()
        if pw_existed[0][0] is None:
            return True
        if pw_existed[0][0] == pw_input:
            return True
        else:
            return False


def list_of_student(sno):  # 根据借书证号查询学生个人信息
    sql = "select * from Student where sno = '%s'" % sno
    cur.execute(sql)
    result = cur.fetchall()
    return result


def list_of_student2(SN):  # 根据姓名搜索用户
    sql = "select * from Student where SNA like '%%%%%s%%%%'" % SN
    cur.execute(sql)
    result = cur.fetchall()
    row = cur.rowcount
    vol = len(result)
    return result


def SelectALLBook():  # 查询所有图书信息
    sql = "select * from Book"
    cur.execute(sql)
    result = cur.fetchall()
    row = len(result)
    vol = len(result[0])
    return result, row, vol


def SelectBorrowInformation(SNO):  # 查询借阅信息
    sql = "select * from Borrow where SNO ='%s'" % SNO
    cur.execute(sql)
    result = cur.fetchall()
    row = cur.rowcount
    vol = 0
    if row != 0:
        vol = len(result[0])
    return result, row, vol


def SelectBorrowInformation2(SNO):  # 选出未归还的图书
    sql = "select * from Borrow where SNO ='%s' and DA3 is null" % SNO
    cur.execute(sql)
    result = cur.fetchall()
    row = cur.rowcount
    vol = 0
    if row != 0:
        vol = len(result[0])
    return result, row, vol


def check_Borrow(BNO, SNO):  # 查阅借书表
    sql = "select * from Borrow where BNO = '%s' and SNO = '%s'" % (BNO, SNO)
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    p = True
    for i in range(len(result)):
        if result[i][6] is None:
            p = False
    return p


def Borrow_Book(BNO, SNO, BookName):  # 添加借书记录，BNO为图书编号，SNO为借书证号，BookName为图书名称
    i = datetime.datetime.now()
    now_date = datetime.timedelta(days=60)
    a = i + now_date
    ID = str(i.year) + str(i.month).zfill(2) + str(i.day).zfill(2) + str(i.minute).zfill(2) + str(i.second).zfill(2)
    DA1 = str(i.year) + '-' + str(i.month).zfill(2) + '-' + str(i.day).zfill(2)
    DA2 = str(a.year) + '-' + str(a.month).zfill(2) + '-' + str(a.day).zfill(2)
    sql = "insert into Borrow (SNO,BNO,BNA,DA1,DA2,Fine,ID) values('%s','%s','%s','%s','%s',0,'%s')" % (
        SNO, BNO, BookName, DA1, DA2, ID)
    try:
        cur.execute(sql)
        cur.connection.commit()
        sql = "update Book set BQS=BQS-1 where BNO='%s'" % BNO
        cur.execute(sql)
        cur.connection.commit()
    except Exception as e:
        print(e)
        print("数据库语句执行错误")
        return False
    else:
        return True


def Select_Part_Book(bookname):  # 搜索指定图书，采用模糊搜索
    sql = "select * from Book where BNA like '%%%%%s%%%%'" % bookname
    cur.execute(sql)
    result = cur.fetchall()
    return result


def AdLogin(UserName, PassWord):  # 判读管理员登录是否满足条件
    sql = "select APW ,AN from Administrator where ANO = '%s'" % UserName
    cur.execute(sql)
    result = cur.fetchall()
    return result


def UpdateUsersInformation(p, In, SNO):  # 更新用户信息
    if p == 0:
        return False
    if p == 1:
        sql = "update Student set SNA = '%s' where SNO = '%s'" % (In, SNO)
    elif p == 2:
        sql = "update Student set SDE = '%s' where SNO = '%s'" % (In, SNO)
    elif p == 3:
        sql = "update Student set SSP = '%s' where SNO = '%s'" % (In, SNO)
    elif p == 4:
        sql = "update Student set SUP = '%d' where SNO = '%s'" % (int(In), SNO)
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
        print("SQL语句执行错误！")
        return False
    else:
        cur.connection.commit()
        return True


def Deleteuser(SNO):  # 删除用户
    sql = "delete from Borrow where SNO ='%s'" % SNO
    sql2 = "delete from Student where SNO='%s'" % SNO
    try:
        cur.execute(sql)
        cur.connection.commit()
    except Exception as e:
        print(e)
        return False
    else:
        try:
            cur.execute(sql2)
            cur.connection.commit()
        except Exception as E:
            print(E)
            print("删除失败")
            return False
        else:
            return True


def InsertIntoBooks(BNO, BNA, BDA, BPU, BPL, BNU):  # 向Book表插入图书
    sql = "insert into Book values('%s','%s','%s','%s','%s','%d','%d')" % (BNO, BNA, BDA, BPU, BPL, int(BNU), int(BNU))
    try:
        cur.execute(sql)
        cur.connection.commit()
    except Exception as e:
        print(e)
        print("sql语句执行错误！")
        return False
    else:
        return True


def ReturnBooks(p, SNO):  # 还书功能

    result, row, vol = SelectBorrowInformation2(SNO)
    sql = None
    sql1 = None
    i = datetime.datetime.now()  # 还书日期
    DA1 = str(i.year) + '-' + str(i.month).zfill(2) + '-' + str(i.day).zfill(2)
    if p == 1:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[0][7])  # 将DA3修改为还书当天的日期，以便于查阅
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[0][0]
    if p == 2:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[1][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[1][0]
    if p == 3:
        sql = "update Borrow set DA3 = '%s' where ID ='%s'" % (
            DA1, result[2][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[2][0]
    if p == 4:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[3][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[3][0]
    if p == 5:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[4][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[4][0]
    if p == 6:
        sql = "update Borrow set DA3 = '%s' where ID ='%s'" % (
            DA1, result[5][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[5][0]
    try:
        cur.execute(sql)
        cur.connection.commit()
        cur.execute(sql1)
        cur.connection.commit()
    except Exception as e:
        print(e)
        print("数据据语句执行错误")
        return False
    else:
        return True


def ReturnBooks2(p, result):  # 还书功能

    sql = None
    sql1 = None
    i = datetime.datetime.now()  # 还书日期
    DA1 = str(i.year) + '-' + str(i.month).zfill(2) + '-' + str(i.day).zfill(2)
    if p == 1:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[0][7])  # 将DA3修改为还书当天的日期，以便于查阅
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[0][0]
    if p == 2:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[1][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[1][0]
    if p == 3:
        sql = "update Borrow set DA3 = '%s' where ID ='%s'" % (
            DA1, result[2][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[2][0]
    if p == 4:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[3][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[3][0]
    if p == 5:
        sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
            DA1, result[4][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[4][0]
    if p == 6:
        sql = "update Borrow set DA3 = '%s' where ID ='%s'" % (
            DA1, result[5][7])
        sql1 = "update Book set BQS = BQS+1 where BNO ='%s'" % result[5][0]
    try:
        cur.execute(sql)
        cur.connection.commit()
        cur.execute(sql1)
        cur.connection.commit()
    except Exception as e:
        print(e)
        print("数据据语句执行错误")
        return False
    else:
        return True


def UpdateFine(SNO, BNO, ID, fine):  # 更新对应图书的罚款信息
    sql = "update Borrow set Fine = '%.2f' where SNO = '%s' and BNO = '%s'and ID='%s'" % (fine, SNO, BNO, ID)
    try:
        cur.execute(sql)
        cur.connection.commit()
    except Exception as e:
        print(e)
        print("数据库语句执行错误！")
        return False
    else:
        print("修改成功！")
        return True


def GetPassword(SNO):
    sql = "select Password from Student where SNO = '%s'" % SNO
    OldPassword = None
    p = True
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
        print("SQL语句错误")
        p = False
    else:
        result = cur.fetchall()
        OldPassword = result[0][0]
    finally:
        return OldPassword, p


def UpdatePassword(SNO, newPassword):  # 更新密码
    sql = "update Student set Password = '%s' where SNO ='%s'" % (newPassword, SNO)
    try:
        cur.execute(sql)
        cur.connection.commit()
    except Exception as e:
        print(e)
        print("修改密码")
        return False
    else:
        return True


def Renewthebook(SNO, BNO, result):
    ID = None
    k = 0
    for i in range(len(result)):
        if result[i][0] == BNO:
            ID = result[i][7]
            k = i
    i = datetime.datetime.now()  # 还书日期
    DA1 = str(i.year) + '-' + str(i.month).zfill(2) + '-' + str(i.day).zfill(2)  # 当天时间
    sql = "update Borrow set DA3 = '%s' where  ID ='%s'" % (
        DA1, ID)  # 将DA3修改为还书当天的日期，以便于查阅
    try:
        cur.execute(sql)
        cur.connection.commit()
    except Exception as e:
        print(e)
        print("续借sql语句错误")
        return False
    else:
        Borrow_Book(BNO, SNO, result[k][2])
        return True
