import pymysql

db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000,charset='utf8')

cursor = db.cursor()


sch = ["周五晚上","下周一","下周三"]
name = ["锻刀","战兽山","燕然峰"]
time = ["23:00","19:30","19:30"]

type = ["丐帮","藏剑","霸刀","剑纯","苍云","丐帮","藏剑","霸刀","剑纯","惊羽","大师","冰心","花间","气纯","毒经","大师","冰心","花间","奶花","奶秀","明尊","铁牢","洗髓","奶歌","奶毒"]
type2 = ["丐帮","藏剑","霸刀","剑纯","苍云","丐帮","藏剑","霸刀","剑纯","惊羽","大师","冰心","花间","气纯","毒经","大师","冰心","花间","奶花","奶秀","明尊","铁牢","洗髓","奶歌","奶毒"]
type3 = ["外功","外功","外功","外功","外功","内功","内功","内功","内功","内功","内功","内功","内功","内功","内功","明尊","奶秀","奶花","奶毒","老板","老板","老板","老板","老板","老板"]

for i in range(len(sch)):
    sql = """INSERT INTO schedule VALUES ('%s', '%s', '%s', 0)"""%(sch[i],name[i],time[i])
    cursor.execute(sql)
    print("Added")
    for j in range(1,26):
        if name[i] != "锻刀":
            sql = """INSERT INTO playerinfo VALUES ('%s', %d, '%s', '', '')"""%(sch[i],j,type[j-1])
        else:
            sql = """INSERT INTO playerinfo VALUES ('%s', %d, '%s', '', '')"""%(sch[i],j,type3[j-1])
        cursor.execute(sql)
        
db.commit()
db.close()