import pymysql

db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000,charset='utf8')

cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS playerinfo")
cursor.execute("DROP TABLE IF EXISTS schedule")

sql = """CREATE TABLE schedule (
         sch CHAR(64),
         name CHAR(64),
         time CHAR(64),
         mygroup CHAR(64),
         num INT ) DEFAULT CHARSET utf8"""
cursor.execute(sql)

sql = """CREATE TABLE playerinfo (
         sch CHAR(64),
         id INT,
         type CHAR(64),
         uid CHAR(64),
         mygroup CHAR(64),
         name CHAR(64) ) DEFAULT CHARSET utf8"""
cursor.execute(sql)
        
db.commit()
db.close()