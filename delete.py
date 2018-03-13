import pymysql

db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000,charset='utf8')

cursor = db.cursor()

sql = """DELETE FROM schedule WHERE sch = '周五'"""
cursor.execute(sql)

sql = """DELETE FROM playerinfo WHERE sch = '周五'"""
cursor.execute(sql)
        
db.commit()
db.close()