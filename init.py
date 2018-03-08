import pymysql

db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000,charset='utf8')

cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS playerinfo")
cursor.execute("DROP TABLE IF EXISTS schedule")

sch = ["周五"]
name = ["战兽山"]
time = ["13:30"]

type = ["丐帮","藏剑","霸刀","剑纯","苍云","丐帮","藏剑","霸刀","剑纯","惊羽","大师","冰心","花间","气纯","毒经","大师","冰心","花间","奶花","奶秀","明尊","铁牢","洗髓","奶歌","奶毒"]



















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

for i in range(len(sch)):
    sql = """INSERT INTO schedule VALUES ('%s', '%s', '%s', 0)"""%(sch[i],name[i],time[i])
    cursor.execute(sql)
    print("Added")
    for j in range(1,26):
        sql = """INSERT INTO playerinfo VALUES ('%s', %d, '%s', '', '')"""%(sch[i],j,type[j-1])
        cursor.execute(sql)
        
db.commit()
db.close()