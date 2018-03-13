import pymysql

db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000,charset='utf8')
cursor = db.cursor()

db2 = pymysql.connect("127.0.0.1","root","testpwd1","test",port=3306,charset='utf8')
cursor2 = db2.cursor()

cursor2.execute("DROP TABLE IF EXISTS playerinfo")
cursor2.execute("DROP TABLE IF EXISTS schedule")
cursor2.execute("DROP TABLE IF EXISTS members")

sql = """CREATE TABLE schedule (
         sch CHAR(64),
         name CHAR(64),
         time CHAR(64),
         mygroup CHAR(64),
         num INT ) DEFAULT CHARSET utf8"""
cursor2.execute(sql)

sql = """CREATE TABLE playerinfo (
         sch CHAR(64),
         id INT,
         type CHAR(64),
         uid CHAR(64),
         mygroup CHAR(64),
         name CHAR(64) ) DEFAULT CHARSET utf8"""
cursor2.execute(sql)

sql = """CREATE TABLE members (
         name CHAR(64),
         title CHAR(64),
         type1 CHAR(64),
         type2 CHAR(64),
         type3 CHAR(64),
         type4 CHAR(64),
         type5 CHAR(64),
         type6 CHAR(64),
         type7 CHAR(64),
         type8 CHAR(64),
         type9 CHAR(64),
         type10 CHAR(64),
         type11 CHAR(64),
         type12 CHAR(64),
         type13 CHAR(64),
         type14 CHAR(64),
         type15 CHAR(64),
         type16 CHAR(64),
         type17 CHAR(64),
         type18 CHAR(64),
         type19 CHAR(64),
         type20 CHAR(64),
         type21 CHAR(64),
         type22 CHAR(64),
         type23 CHAR(64),
         type24 CHAR(64),
         type25 CHAR(64)) DEFAULT CHARSET utf8"""
cursor2.execute(sql)

sql = """SELECT * FROM schedule"""
cursor2.execute(sql)
result = cursor.fetchall()
for line in result:
    sql = """INSERT INTO schedule VALUES ('%s', '%s', '%s', '%s', %d)"""%line
    cursor2.execute(sql)
    
sql = """SELECT * FROM playerinfo"""
cursor.execute(sql)
result = cursor.fetchall()
for line in result:
    sql = """INSERT INTO playerinfo VALUES ('%s', %d, '%s', '%s', '%s', '%s')"""%line
    cursor2.execute(sql)

sql = """SELECT * FROM members"""
cursor.execute(sql)
result = cursor.fetchall()
for line in result:
    sql = """INSERT INTO members VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""%line
    cursor2.execute(sql)
    
db.commit()
db.close()     
db2.commit()
db2.close()
