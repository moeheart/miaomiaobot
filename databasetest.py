import pymysql

db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000 )

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

sql = """CREATE TABLE testt (
         NAME  CHAR(20) ,
         uid CHAR(20),
         id INT )"""
cursor.execute(sql)

sql = """INSERT INTO testtt VALUES ('myname', '12345', 1)"""
cursor.execute(sql)

sql = """SELECT * from testt"""
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    print(row)

db.close()