import PyMySQL

db = MySQLdb.connect("172.21.0.10","root","testpwd1","test" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# 创建数据表SQL语句
sql = """CREATE TABLE testt (
         NAME  CHAR(20) ,
         uid CHAR(20),
         id INT )"""
cursor.execute(sql)

sql = """INSERT INTO testtt VALUES ('myname', '12345', 1)"""
cursor.execute(sql)

sql = """SELECT * from test"""
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    print(row)

# 关闭数据库连接
db.close()