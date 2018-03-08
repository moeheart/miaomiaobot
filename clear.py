import pymysql

db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000,charset='utf8')

cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS playerinfo")
cursor.execute("DROP TABLE IF EXISTS schedule")

sql = """CREATE TABLE schedule (
         sch CHAR(30),
         name CHAR(30),
         time CHAR(30),
         num INT ) DEFAULT CHARSET utf8"""
cursor.execute(sql)

sql = """CREATE TABLE playerinfo (
         sch CHAR(32),
         id INT,
         type CHAR(32),
         uid CHAR(32),
         name CHAR(32) ) DEFAULT CHARSET utf8"""
cursor.execute(sql)
        
db.commit()
db.close()