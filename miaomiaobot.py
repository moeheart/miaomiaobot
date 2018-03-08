# coding:utf-8
from flask import Flask    
from flask import request    
from flask import make_response,Response
import json
import read
import re
import pymysql

app = Flask(__name__) 
app.config['JSON_AS_ASCII'] = False

def Response_headers(content):    
    resp = Response(content)    
    resp.headers['Access-Control-Allow-Origin'] = '*'    
    return resp
    
@app.route('/', methods=['POST'])    
def handle():    
    jdata = request.json
    content = jdata["content"]
    print(jdata["content"])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    nickname = {
    "丐帮":"丐帮",
    "丐丐":"丐帮",
    "笑尘诀":"丐帮",
    "藏剑":"藏剑",
    "黄鸡":"藏剑",
    "黄叽":"藏剑",
    "问水诀":"藏剑",
    "山居剑意":"藏剑",
    "霸刀":"霸刀",
    "北傲诀":"霸刀",
    "剑纯":"剑纯",
    "剑咩":"剑纯",
    "太虚剑意":"剑纯",
    "苍云":"苍云",
    "铁骨":"苍云",
    "苍云T":"苍云",
    "铁骨衣":"苍云",
    "分山劲":"苍云",
    "惊羽":"惊羽",
    "鲸鱼":"惊羽",
    "惊羽诀":"惊羽",
    "大师":"大师",
    "易筋经":"大师",
    "秃子":"大师",
    "冰心":"冰心",
    "冰心诀":"冰心",
    "花间":"花间",
    "花间游":"花间",
    "气纯":"气纯",
    "气咩":"气纯",
    "紫霞功":"气纯",
    "毒经":"毒经",
    "奶花":"奶花",
    "花奶":"奶花",
    "离经易道":"奶花",
    "离经":"奶花",
    "奶秀":"奶秀",
    "秀奶":"奶秀",
    "云裳":"奶秀",
    "云裳心经":"奶秀",
    "明尊":"明尊",
    "明尊琉璃体":"明尊",
    "明教":"明尊",
    "明教T":"明尊",
    "喵T":"明尊",
    "铁牢":"铁牢",
    "天策":"铁牢",
    "天策T":"铁牢",
    "策T":"铁牢",
    "汪T":"铁牢",
    "狗T":"铁牢",
    "铁牢律":"铁牢",
    "洗髓":"洗髓",
    "洗髓经":"洗髓",
    "大师T":"洗髓",
    "奶歌":"奶歌",
    "歌奶":"奶歌",
    "相知":"奶歌",
    "奶毒":"奶毒",
    "毒奶":"奶毒",
    "补天诀":"奶毒",
    "补天":"奶毒"}
    
    replycontent = ''
    
    print(jdata)
    savedGroup = ['miaomiao测试群','【千衷】团本通知群']
    if ("group" in jdata.keys()) and (jdata["group"] in savedGroup): 
        db = pymysql.connect("172.21.0.10","root","testpwd1","test",port=5000,charset='utf8')
        cursor = db.cursor()
        res = re.search("^(.*)报名(.*)$", content)
        if res:
            if res.group(1) in nickname.keys():
                type = nickname[res.group(1)]
                sch = res.group(2)
                sql = """SELECT sch, num from schedule WHERE sch = '%s'"""%sch
                cursor.execute(sql)
                result0 = cursor.fetchall()
                if (result0):
                    sql = """SELECT id, uid, name from playerinfo WHERE sch = '%s' AND type = '%s'"""%(sch,type)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    flag = 0
                    id = 0
                    others = ' '
                    for line in result:
                        if line[1] == '':
                            flag = 1
                            id = line[0]
                            break
                        elif line[1] == jdata["sender_id"]:
                            flag = 2
                            replycontent = '%s，你已经报过名啦'%jdata["sender"]
                        else:
                            others = others + line[2] + ' '
                    if flag == 0:
                        replycontent = '没有坑啦，去找%s打一架吧'%others
                    elif flag == 1:
                        sql = """UPDATE playerinfo SET uid = '%s', name = '%s' WHERE sch = '%s' AND id = %d """%(jdata["sender_id"],jdata["sender"],sch,id)
                        cursor.execute(sql)
                        sql = """UPDATE schedule SET num = %d WHERE sch = '%s'"""%(result0[0][1],sch)
                        cursor.execute(sql)
                        replycontent = '报名成功！id为%d'%id
                    
        res = re.search("^有(什么本|本吗)？?$", content)
        if res:
            first = 1
            sql = """SELECT sch, name, time, num from schedule"""
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for line in result:
                    if (first):
                        first = 0
                    else:
                        replycontent = replycontent + '\n'
                        replycontent = replycontent + '【%s】有 %s ，时间%s，已报名%d人'%(line[0],line[1],line[2],line[3])
            else:
                replycontent = '团长咸鱼去了，并没有本'
                
        res = re.search("^(.*)报名情况$", content)
        if res:
            sch = res.group(1)
            sql = """SELECT sch, name, num from schedule WHERE sch = '%s'"""%sch
            cursor.execute(sql)
            result0 = cursor.fetchall()
            if (result0):
                first = 1
                sql = """SELECT id, type, name from playerinfo WHERE sch = '%s'"""%(sch)
                cursor.execute(sql)
                result = cursor.fetchall()
                replycontent = '%s %s已报名%d人'%(sch,result0[0][1],result0[0][2])
                for line in result:
                    replycontent = replycontent + '\n'
                    replycontent = replycontent + '%d %s: %s'%(line[0],line[1],line[2])
                    
        res = re.search("^取消报名$", content)
        if res:
            sch = res.group(1)
            sql = """SELECT sch, id from playerinfo WHERE uid = '%s'"""%jdata["sender_id"]
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                sql = """UPDATE playerinfo SET uid = '', name = '' WHERE uid = %s"""%jdata["sender_id"]
                cursor.execute(sql)
                result = cursor.fetchall()
                replycontent = '取消成功！江湖不见！'
                minus = {}
                for line in result:
                    if (line[0] not in minus.keys()):
                        minus[line[0]] = -1
                    else:
                        minus[line[0]] -= 1
            for sch in minus.keys():
                sql = """SELECT num from schedule WHERE sch = '%s'"""%sch
                cursor.execute(sql)
                result = cursor.fetchall()
                sql = """UPDATE schedule SET num = %d WHERE sch = %s"""%(result[0][0]+minus[sch], sch)
                cursor.execute(sql)          
                
    if replycontent != '':
        replydata = [{'reply':replycontent}]
        return jsonify(replydata)
    
    return ''
    
if __name__ == '__main__':
    import signal
    create_rotating_log('logs/miaomiao.log')
    app.run(host='0.0.0.0', port=8888)