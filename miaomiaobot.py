# coding:utf-8
from flask import Flask, jsonify 
from flask import request    
from flask import make_response,Response
from urllib import quote
import json
import read
import re
import pymysql
import random
import urllib.request

app = Flask(__name__) 
app.config['JSON_AS_ASCII'] = False

def Response_headers(content):    
    resp = Response(content)    
    resp.headers['Access-Control-Allow-Origin'] = '*'    
    return resp
    
def updateid():
    app.adminlist = []
    app.admininfo = {}
    response = urllib.request.urlopen('http://127.0.0.1:5000/openqq/get_friend_info')
    html = response.read()
    jsonf = json.loads(html.decode())
    for line in jsonf:  
        app.admininfo[line["name"]] = {'id': line["id"]}
        app.adminlist += [line["id"]]
    
    response = urllib.request.urlopen('http://127.0.0.1:5000/openqq/get_group_basic_info')
    html = response.read()
    jsonf = json.loads(html.decode())
    for line in jsonf:  
        if line["id"] in app.info.keys():
            app.info[line["name"]]['id'] = line["id"]
        
    print(app.admininfo)
    print(app.adminlist)
    print(app.ownGroup)
    
def setnickname():
    nicknamelist = {
    "丐帮":["丐帮","丐丐","笑尘诀"],
    "藏剑":["问小水","山小居","藏剑","黄鸡","黄叽","问水诀","问水","藏剑","山居剑意","山居","黄焖鸡"],
    "霸刀":["霸小刀","霸刀","北傲诀"],
    "剑纯":["剑纯","剑咩","太虚剑意"],
    "气纯":["气纯","气咩","紫霞功"],
    "苍云":["苍云","铁骨","苍云T","苍云t","铁骨衣","苍云wifi","wifi"],
    "分山":["分山劲","分山","岔劲"],
    "惊羽":["惊小羽","惊羽","鲸鱼","惊羽诀"],
    "田螺":["天罗","田螺","天罗诡道"],
    "大师":["大师","易筋经","易筋","秃子","和尚","少林","秃驴","灯泡","圣僧","易经"],
    "冰心":["冰小心","冰心","冰心诀","七秀"],
    "花间":["花小间","花间游","万花"],
    "毒经":["毒小经","毒经","五毒"],
    "莫问":["莫小问","莫问","长歌"],
    "奶花":["离小经","奶花","花奶","离经易道","离经"],
    "奶秀":["云小裳","奶秀","秀奶","云裳心经","云裳"],
    "奶毒":["补天","奶毒","毒奶","补天诀","补天"],
    "奶歌":["相小知","奶歌","歌奶","相知","奶鸽","鸽奶","乳鸽"],
    "焚影":["焚小影","焚影","焚影圣诀"],
    "明尊":["明尊","明尊琉璃体","明教","明教T","明教t","喵T","喵t"],
    "傲血":["傲小雪","傲雪","傲血","傲血战意"],
    "铁牢":["铁牢","铁牢律","天策","天策T","天策t","策T","策t","狗T","狗t"],
    "洗髓":["洗髓","洗髓经","大师T","大师t","秃T","秃t","和尚T","和尚t"],
    "力道":["力道",],
    "身法":["身法",],
    "元气":["元气",],
    "根骨":["根骨",],
    "奶妈":["奶妈",],
    "T":["T","t"],
    "老板":["老板",],
    "外功":["外功",],
    "内功":["内功",],
    }
    nickname = {}
    for x in nicknamelist.keys():
        for y in nicknamelist[x]:
            nickname[y] = x
    app.nickname = nickname
    
@app.route('/', methods=['POST'])    
def handle():    
    jdata = request.json
    content = jdata["content"]
    if content is None:
        return ''
    if content[0:10] != "@miaomiao ":
        pass#return ''
    else:
        content = content[10:]
    print(content)
    
    nickname = app.nickname
    typename = {
    "丐帮":"力道",
    "藏剑":"身法",
    "霸刀":"力道",
    "傲血":"力道",
    "剑纯":"身法",
    "分山":"身法",
    "惊羽":"力道",
    "大师":"元气",
    "冰心":"根骨",
    "花间":"元气",
    "田螺":"元气",
    "焚影":"元气",
    "气纯":"根骨",
    "毒经":"根骨",
    "奶花":"奶妈",
    "奶秀":"奶妈",
    "明尊":"T",
    "铁牢":"T",
    "洗髓":"T",
    "苍云":"T",
    "莫问":"根骨",
    "奶歌":"奶妈",
    "奶毒":"奶妈",
    "力道":"力道",
    "身法":"身法",
    "元气":"元气",
    "根骨":"根骨",
    "奶妈":"奶妈",
    "T":"T",
    "老板":"老板",
    "外功":"外功",
    "内功":"内功"}
    
    replycontent = ''
    
    print(jdata)
    ownGroup = app.ownGroup
    savedGroup = app.savedGroup
    groupLink = app.groupLink
    
    db = pymysql.connect("127.0.0.1","root","testpwd1","test",port=3306,charset='utf8')
    cursor = db.cursor()
    
    if ("group" in jdata.keys()) and (jdata["group"] in savedGroup): 
        if content == "使用说明":
            replycontent = "1.查询团本情况\n示例：有本吗\n2.报名团本\n示例：奶花报名周五\n3.查询报名情况\n示例：周五报名情况\n4.取消报名\n示例：取消报名周五\n5.查询小药/奇穴/宏\n示例：花间宏"
        group = jdata["group"]
        group = groupLink[group]
        
        if (app.info[jdata["group"]]["smoke"] == 1):
            res = re.search("傻逼|弱智|你妈死了", content)
            if res:
                replycontent = "请文明发言，和谐用语！"    
                replydata = {'reply':replycontent, 'shutup': 1, "shutup_time": 180}
                return jsonify(replydata)
                
        res = re.search("^(无敌)?(.+)报名(.+?)( id(.+))?$", content)
        if res:
            if res.group(2) in ['纯阳']:
                replycontent = '剑纯还是气纯？'
            elif res.group(2) in ['长歌']:
                replycontent = '莫问还是奶歌？'
            elif res.group(2) in ['七秀','秀秀']:
                replycontent = '冰心还是奶秀？'
            elif res.group(2) in ['万花','花花']:
                replycontent = '花间还是奶花？'
            elif res.group(2) in nickname.keys():
                type = nickname[res.group(2)]
                sch = res.group(3)
                gameid = ''
                if res.group(5) is not None:
                    gameid = res.group(5)
                sql = """SELECT sch, num from schedule WHERE sch = '%s' AND mygroup = '%s'"""%(sch,group)
                cursor.execute(sql)
                result0 = cursor.fetchall()
                if (result0):
                    sql = """SELECT id, uid, name from playerinfo WHERE sch = '%s' AND type = '%s' AND mygroup = '%s'"""%(sch,type,group)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    flag = 0
                    id = 0
                    others = ' '
                    if result:
                        for line in result:
                            if line[2] == '':
                                flag = 1
                                id = line[0]
                                break
                            elif line[1] == str(jdata["sender_id"]):
                                flag = 2
                                replycontent = '%s，你已经报过名啦'%jdata["sender"]
                            else:
                                others = others + line[2] + ' '
                    if flag == 0:
                        if others == ' ':
                            if type == '傲血':
                                replycontent = '傲血还能进本？切T去吧'
                            elif type == '焚影':
                                replycontent = '焚影还能进本？切T去吧'
                            elif type == '分山':
                                replycontent = '分山还能进本？打wifi吧'
                            elif type == '田螺':
                                replycontent = '田螺还能进本？下个版本见吧'
                            else:
                                replycontent = '你确定你的职业能进本吗？'
                        else:
                            replycontent = '没有坑啦，去找%s打一架吧'%others
                    elif flag == 1:
                        sql = """UPDATE playerinfo SET uid = '%s', name = '%s', gameid = '%s' WHERE sch = '%s' AND id = %d AND mygroup = '%s'"""%(jdata["sender_id"],jdata["sender"],gameid,sch,id,group)
                        cursor.execute(sql)
                        sql = """UPDATE schedule SET num = %d WHERE sch = '%s' AND mygroup = '%s'"""%(result0[0][1]+1,sch,group)
                        cursor.execute(sql)
                        replycontent = '%s 报名成功！id为%d'%(type,id)
                    
        res = re.search("有(什么本|本吗|本嘛)", content)
        if res:
            first = 1
            sql = """SELECT sch, name, time, num from schedule WHERE mygroup = '%s'"""%group
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
                
        res = re.search("^(.+)报名情况$", content)
        if res:
            sch = res.group(1)
            sql = """SELECT sch, name, num from schedule WHERE sch = '%s' AND mygroup = '%s'"""%(sch,group)
            cursor.execute(sql)
            result0 = cursor.fetchall()
            if (result0):
                first = 1
                sql = """SELECT id, type, name, gameid from playerinfo WHERE sch = '%s' AND mygroup = '%s'"""%(sch,group)
                cursor.execute(sql)
                result = cursor.fetchall()
                replycontent = '%s %s已报名%d人'%(sch,result0[0][1],result0[0][2])
                for line in result:
                    replycontent = replycontent + '\n'
                    replycontent = replycontent + '%d %s: %s'%(line[0],line[1],line[2])
                    if (line[3] is not None) and (line[3] != ''):
                        replycontent = replycontent + 'id%s'%line[3]
                    
        res = re.search("^取消报名$", content)
        if res:
            p = random.randint(1,10)
            if p <= 2:
                replycontent = random.choice(["你脸太黑了，取消失败！","你说取消就取消？","放鸽子是不对的！","就不取消，你来打我呀"])
            else:
                minus = {}
                sql = """SELECT sch, id, type from playerinfo WHERE name = '%s' AND mygroup = '%s'"""%(jdata["sender"],group)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    type = result[0][2]
                    sql = """UPDATE playerinfo SET uid = '', name = '', gameid = '' WHERE name = '%s' AND mygroup = '%s'"""%(jdata["sender"],group)
                    cursor.execute(sql)
                    replycontent = '%s 取消成功！江湖不见！'%type
                    for line in result:
                        if (line[0] not in minus.keys()):
                            minus[line[0]] = -1
                        else:
                            minus[line[0]] -= 1
                for sch in minus.keys():
                    sql = """SELECT num from schedule WHERE sch = '%s' AND mygroup = '%s'"""%(sch,group)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    sql = """UPDATE schedule SET num = %d WHERE sch = '%s' AND mygroup = '%s'"""%(result[0][0]+minus[sch], sch, group)
                    cursor.execute(sql)  
                    
        res = re.search("^取消报名(.+)$", content)
        if res:
            p = random.randint(1,10)
            if p <= 2:
                replycontent = random.choice(["你脸太黑了，取消失败！","你说取消就取消？","放鸽子是不对的！","就不取消，你来打我呀"])
            else:
                minus = {}
                sql = """SELECT sch, id from playerinfo WHERE name = '%s' AND sch = '%s' AND mygroup = '%s'"""%(jdata["sender"],res.group(1),group)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    sql = """UPDATE playerinfo SET uid = '', name = '' WHERE name = '%s' AND sch = '%s' AND mygroup = '%s'"""%(jdata["sender"],res.group(1),group)
                    cursor.execute(sql)
                    replycontent = '取消成功！江湖不见！'
                    minus = {}
                    for line in result:
                        if (line[0] not in minus.keys()):
                            minus[line[0]] = -1
                        else:
                            minus[line[0]] -= 1
                for sch in minus.keys():
                    sql = """SELECT num from schedule WHERE sch = '%s' AND mygroup = '%s'"""%(sch,group)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    sql = """UPDATE schedule SET num = %d WHERE sch = '%s' AND mygroup = '%s'"""%(result[0][0]+minus[sch], sch, group)
                    cursor.execute(sql)  
    
    if ("sender" in jdata.keys()) and (jdata["sender_id"] in app.adminlist):
        name = jdata["sender"]
        time = time = int(jdata['time'])
        if (app.info[jdata["group"]]["help"] == 1):
            res = re.search("^互助 (.+)$", content)
            if res:
                message = res.group(1)
                if len(message) > 50:
                    replycontent = "消息过长，请控制在50个字符以内~"
                elif app.info[jdata["group"]]['cd'] > time:
                    replycontent = "该群的发起互助处于cd中，剩余%d秒"%(time - app.info[jdata["group"]]['cd'])
                elif app.overallcd > time:
                    replycontent = "发起互助处于公共cd中，剩余%d秒"%(time - overallcd)
                else:
                    app.overallcd = time + 300
                    app.info[jdata["group"]['cd']] = time + 10800
                    for group in info.keys():
                        if group['help'] == 1:
                            response = urllib.request.urlopen('http://127.0.0.1:5000/openqq/send_group_message?id=%s&content=%s&async=1'%(group['id'],quote(message))
        
        if content == "团长使用说明":
            replycontent = "1.新建团本\n示例：开团 周五 战兽山 13:00 战兽山参考配置\n2.关闭团本\n示例：结束 周五\n3.修改报名信息\n示例：报名 周五 左渭雨 22\n4.删除报名信息\n示例：取消 周五 22\n5.更换职业信息\n示例：更换 周五 洗髓 22\n6.更改团名/内容/时间\n示例：改名 周五 周六\n7.个性化配置(高级)\n示例：新建配置 战兽山2:分山 田螺 焚影 (以下省略)\n注意：如果管理多个群，可以在指令最后加空格和数字，表示第几个群（默认为0）。"
        res = re.search("^开团 (.+?) (.+?) (.+?) (.+?)( (.+))?$", content)
        if res:
            if res.group(6) is not None:
                group = ownGroup[name][int(res.group(6))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:
                group = ownGroup[name][0]
            sql = """SELECT * FROM schedule WHERE sch = '%s' AND mygroup = '%s'"""%(res.group(1),group)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                replycontent = "团名已存在，请换一个试试"
            else:
                sql = """SELECT * FROM members WHERE title = '%s' AND (name = '%s' OR name = 'everyone')"""%(res.group(4),name)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    type = result[0]
                    sql = """INSERT INTO schedule VALUES ('%s', '%s', '%s', '%s', 0)"""%(res.group(1), res.group(2), res.group(3), group)
                    cursor.execute(sql)
                    for i in range(1,26):
                        sql = """INSERT INTO playerinfo VALUES ('%s', %d, '%s', '', '%s', '', '')"""%(res.group(1), i, type[i+1], group)
                        cursor.execute(sql)
                    replycontent = '开团成功！'
                else:
                    replycontent = '开团失败，请确认配置信息是否正确'
                    
        res = re.search("^结束 (.+?)( (.+))?$", content)
        if res:  
            if res.group(3) is not None:
                group = ownGroup[name][int(res.group(3))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:
                group = ownGroup[name][0]
            sql = """SELECT * FROM schedule WHERE sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
            cursor.execute(sql)
            rr = cursor.fetchall()
            if rr:
                sql = """DELETE FROM schedule WHERE sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
                cursor.execute(sql)

                sql = """DELETE FROM playerinfo WHERE sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
                cursor.execute(sql)
                replycontent = '团本已结束！'
            else:
                replycontent = '结束失败，该团本不存在！'
        
        res = re.search("^报名 (.+?) (.+?) (.+?)( (.+))?$", content)
        if res: 
            if res.group(5) is not None:
                group = ownGroup[name][int(res.group(5))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:

                group = ownGroup[name][0]
                
            sql = """SELECT * FROM playerinfo WHERE sch = '%s' AND mygroup = '%s' AND id = %d"""%(res.group(1), group, int(res.group(3)))
            cursor.execute(sql)
            rr = cursor.fetchall()
            if rr:
                sql = """UPDATE playerinfo SET name = '%s' WHERE sch = '%s' AND mygroup = '%s' AND id = %d"""%(res.group(2), res.group(1), group, int(res.group(3)))
                cursor.execute(sql)
                
                sql = """SELECT id from playerinfo WHERE name != '' AND sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
                cursor.execute(sql)
                result = cursor.fetchall()
                num = len(result)
                
                sql = """UPDATE schedule SET num = %d WHERE sch = '%s' AND mygroup = '%s'"""%(num, res.group(1), group)
                cursor.execute(sql)  
                replycontent = '修改报名信息成功！'
            else:
                replycontent = '手动报名失败，该团本/id不存在！'
            
        res = re.search("^取消 (.+?) (.+?)( (.+))?$", content)
        if res: 
            if res.group(4) is not None:
                group = ownGroup[name][int(res.group(4))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:

                group = ownGroup[name][0]
                
            sql = """SELECT * FROM playerinfo WHERE sch = '%s' AND mygroup = '%s' AND id = %d"""%(res.group(1), group, int(res.group(2)))
            cursor.execute(sql)
            rr = cursor.fetchall()
            if rr:
                sql = """UPDATE playerinfo SET name = '', gameid = '' WHERE sch = '%s' AND mygroup = '%s' AND id = %d"""%(res.group(1), group, int(res.group(2)))
                cursor.execute(sql)
                
                sql = """SELECT id from playerinfo WHERE name != '' AND sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
                cursor.execute(sql)
                result = cursor.fetchall()
                num = len(result)
                
                sql = """UPDATE schedule SET num = %d WHERE sch = '%s' AND mygroup = '%s'"""%(num, res.group(1), group)
                cursor.execute(sql)  
                replycontent = '取消报名信息成功！'
            else:
                replycontent = "取消报名失败，该团本/id不存在！"
            
        res = re.search("^改名 (.+?) (.+?)( (.+))?$", content)
        if res:
            if res.group(4) is not None:
                group = ownGroup[name][int(res.group(4))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:
                group = ownGroup[name][0]
            sql = """SELECT * FROM schedule WHERE sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
            cursor.execute(sql)
            rr = cursor.fetchall()
            if rr:
                sql = """UPDATE schedule SET sch = '%s' WHERE sch = '%s'"""%(res.group(2), res.group(1))
                cursor.execute(sql) 
                sql = """UPDATE playerinfo SET sch = '%s' WHERE sch = '%s'"""%(res.group(2), res.group(1))
                cursor.execute(sql) 
                replycontent = '更改团名成功！'
            else:
                replycontent = '更改团名失败，该团本不存在！'
            
        res = re.search("^改内容 (.+?) (.+?)( (.+))?$", content)
        if res:
            if res.group(4) is not None:
                group = ownGroup[name][int(res.group(4))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:

                group = ownGroup[name][0]
            sql = """SELECT * FROM schedule WHERE sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
            cursor.execute(sql)
            rr = cursor.fetchall()
            if rr:
                sql = """UPDATE schedule SET name = '%s' WHERE sch = '%s'"""%(res.group(2), res.group(1))
                cursor.execute(sql) 
                sql = """UPDATE playerinfo SET name = '%s' WHERE sch = '%s'"""%(res.group(2), res.group(1))
                cursor.execute(sql) 
                replycontent = '更改内容成功！'
            else:
                replycontent = '更改内容失败，该团本不存在！'
            
        res = re.search("^改时间 (.+?) (.+?)( (.+))?$", content)
        if res:
            if res.group(4) is not None:
                group = ownGroup[name][int(res.group(4))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:

                group = ownGroup[name][0]
            sql = """SELECT * FROM schedule WHERE sch = '%s' AND mygroup = '%s'"""%(res.group(1), group)
            cursor.execute(sql)
            rr = cursor.fetchall()
            if rr:
                sql = """UPDATE schedule SET time = '%s' WHERE sch = '%s'"""%(res.group(2), res.group(1))
                cursor.execute(sql) 
                sql = """UPDATE playerinfo SET time = '%s' WHERE sch = '%s'"""%(res.group(2), res.group(1))
                cursor.execute(sql) 
                replycontent = '更改时间成功！'
            else:
                replycontent = '更改时间失败，该团本不存在！'
            
        res = re.search("^更换 (.+?) (.+?) (.+?)( (.+))?$", content)
        if res: 
            if res.group(4) is not None:
                group = ownGroup[name][int(res.group(4))]
            elif ("group" in jdata.keys()):
                group = jdata["group"]
            else:
                group = ownGroup[name][0]   
            sql = """SELECT * FROM playerinfo WHERE sch = '%s' AND mygroup = '%s' AND id = %d"""%(res.group(1), group, int(res.group(3)))
            cursor.execute(sql)
            rr = cursor.fetchall()
            if (res.group(2) not in nickname.keys()):
                replycontent = '更换配置失败，该职业不存在！'
            elif rr:
                sql = """UPDATE playerinfo SET type = '%s' WHERE sch = '%s' AND mygroup = '%s' AND id = %d"""%(res.group(2), res.group(1), group, int(res.group(3)))
                cursor.execute(sql)
                replycontent = '更换配置成功！'
            else:
                replycontent = '更换配置失败，该团本/id不存在！'
        
        res = re.search("^新建配置 (.+):(.+)$", content)
        if res: 
            title = res.group(1)
            sql = """SELECT * FROM members WHERE title = '%s' AND name = '%s'"""%(title, name)
            cursor.execute(sql)
            res = cursor.fetchall()
            if res:
                replycontent = '该名称已存在，请换一个试试'
            else:
                str2 = res.group(2).split(' ')
                typelist = []
                if (len(str2) == 25):
                    flag = 1
                    unknown = ""
                    for type in str2:
                        if type not in nickname.keys():
                            flag = 0
                            unknown = type
                            break
                        typelist.append(nickname[type])
                    if flag == 1:
                        sql = """INSERT INTO members VALUES ('%s', '%s'"""%(name, title)
                        for i in range(25):
                            sql += ", '%s'"%typelist[i]
                        sql += ')'
                        print(sql)
                        cursor.execute(sql)
                        replycontent = '新建配置成功！'
                    else:
                        replycontent = '新建配置失败:职业 %s 未知'%unknown
                else:
                    replycontent = '新建配置失败: 长度为 %d'%len(str2)
        
    if True:
        p = random.randint(1,10)
        
        res = re.search("^(.+)(四?)小药$", content)
        if res:
            if (res.group(1) in nickname.keys()):
                type = nickname[res.group(1)]
                typet = typename[type]
                if typet == "力道":
                    replycontent = '力道四小药：\n低配版：[玉璃丹][点骨丹][清凉月霍碎][凤凰胎]\n豪华版：[重置·八仙盘][珍·鸳鸯鸡][重置·玉阳丹][珍·金麟丹]'
                elif typet == "身法":
                    replycontent = '身法四小药：\n低配版：[玉璃丹][轻身丹][清凉月霍碎][小天酥]\n豪华版：[重置·五侯鲭][珍·鸳鸯鸡][重置·御风丹][珍·金麟丹]'
                elif typet == "元气":
                    replycontent = '元气四小药：\n低配版：[白信丹][养神丹][通花软牛肠][长生粥]\n豪华版：[重置·云梦肉][珍·金乳酥][重置·益神丹][珍·养魂丹]'
                elif typet == "根骨":
                    replycontent = '根骨四小药：\n低配版：[白信丹][补心丹][通花软牛肠][汉宫棋]\n豪华版：[重置·葵花鸭][珍·金乳酥][重置·九还丹][珍·养魂丹]'
                elif typet == "奶妈":
                    replycontent = '奶妈四小药：\n低配版：[白信丹][补心丹][通花软牛肠][汉宫棋]\n豪华版：[重置·葵花鸭][珍·金乳酥][重置·九还丹][珍·养魂丹]'
                elif typet == "T":
                    replycontent = 'T吃个毛线的小药！该死的要死啊！'
                if p <= 2: 
                    if type == "藏剑":
                        replycontent = '藏剑四小药：\n[鸡饲料][增肥剂][激素][营养粉]'
                    elif type in ["焚影","明尊"]:
                        replycontent = '明教四小药：\n[初级喵饲料][中级喵饲料][高级喵饲料][特级喵饲料]'
                    elif type in ["傲雪","铁牢"]:
                        replycontent = '天策四小药：\n[皇竹草][甜象草][紫花苜蓿][百脉根]'
        
        res = re.search("^(.+)奇穴$", content)
        if res:
            if (res.group(1) in nickname.keys()):
                type = nickname[res.group(1)]
                if type == "花间":
                    replycontent = '[弹指][雪中行][倚天][青歌][焚玉][青冠][清流][雪弃][生息][梦歌][踏歌][涓流]'
                elif type == "奶花":
                    replycontent = '[弹指][生息][月华][青疏][微潮][千机][束彼][池月][述怀][零落][砚悬][折叶笼花]'
                elif type == "冰心":
                    replycontent = '[明妃][千里冰封][新妆][青梅][枕上][生莲][望舒][元君][霜风][朝露][焕颜][清涓]'
                elif type == "奶秀":
                    replycontent = '[朝露][盛夏][辞致][瑰姿][乞巧][散余霞][晚晴][碎冰][霜风][秋深][焕颜][余寒映日]'
                elif type == "毒经":
                    replycontent = '(死蛇)[尻尾][无常][黯影][虫兽][蟾啸][不鸣][尾后针][祭礼][分澜][蛊虫狂暴][固灵][封丘]\n(不死蛇)[生发][无常][黯影][虫兽][蟾啸][不鸣][尾后针][啖灵][分澜][蛊虫狂暴][固灵][封丘]'
                elif type == "奶毒":
                    replycontent = '[柔丝][仁心][织雾][冰蚕决][桃僵][枭泣][纳精][祭礼][仙王蛊鼎][蝶隐][织心][迷仙引梦]'
                elif type == "莫问":
                    replycontent = '[号钟][飞帆][争簇][殊曲][豪情][师襄][广雅][刻梦][书离][参连][啸影][无尽藏]'
                elif type == "奶歌":
                    replycontent = '(阳春流)[蔚风][秋鸿][争簇][殊曲][谪仙][自赏][寸光阴][明鸾][凝绝][棋宫][掷杯][无尽藏]\n(盾流)[蔚风][秋鸿][争簇][殊曲][寒酒][平吟][笙簧][明鸾][凝绝][庄周梦][大韶][绝唱]'
                elif type == "剑纯":
                    replycontent = '[心固][深埋][化三清][无意][心转][叠刃][切玉][负阴][和光][期声][无欲][行天道]'
                elif type == "气纯":
                    replycontent = '[白虹][霜锋][同尘][无形][天地根][跬步][万物][抱阳][浮生][期声][重光][剑出鸿蒙]'
                elif type == "藏剑":
                    replycontent = '[淘尽][清风][夜雨][映波锁澜][山色][怜光][雾锁][厌高][山重水复][归啼][如风][片玉]'
                elif type == "霸刀":
                    replycontent = '[虎踞][沧雪][疏狂][化蛟][含风][逐鹿][斩纷][星火][楚歌][绝期][冷川][心镜]'
                elif type == "丐帮":
                    replycontent = '[玄黄][御龙][自强][无疆][克己][有攸][满盈][雨龙][不息][复礼][饮江][降龙]'
                elif type == "明尊":
                    replycontent = '[食肉众生][慈悲心][寂灭][月尽天明][超凡入圣][极乐引][极本溯源][辟滞扈沙][渡厄力][光明心][宿角生辉][心火叹]'
                elif type == "铁牢":
                    replycontent = '[定军][龙痕][徐如林][望西京][劲风][掠如火][踏北邙][战心][长征][激雷][载戎][号令三军]'
                elif type == "洗髓":
                    replycontent = '[不垢][大明][大觉][归来去棍][禅语][立地成佛][不畏][明王身][无量][轮回诀][独觉][舍身弘法]'
                elif type == "惊羽":
                    replycontent = '[迅电流光][千里无痕][百步穿杨][摧心][穿林打叶][聚精凝神][夺魄之威][浴血沁骨][鹰扬虎视][回肠荡气][侵火动旌][妙手连环]'
                elif type == "铁骨":
                    replycontent = '[盾威][激昂][践踏][坚铁][振奋][雷云][肆意][返生][寒甲][战毅][肃驾][寒啸千军]'
                elif type == "大师":
                    replycontent = '[心棍][幻身][明法][缩地][降魔渡厄][金刚怒目][三生][华香][众嗔][净果][五识][二业依缘]'
                elif type == "焚影":
                    replycontent = '[腾焰飞芒][净身明礼][洞若观火][无明业火][明光恒照][辉耀红尘][万念俱寂][日月同辉][天地诛戮][寂灭劫灰][伏明众生][驱夷逐法]'
                elif type == "田螺":
                    replycontent = '[天魔蚀肌][劫数难逃][弩击急骤][千机之威][积重难返][聚精凝神][化血迷心][蚀肌化血][秋风散影][千机巨搫][曙色催寒][雷甲三铉]'
                elif type == "分山":
                    replycontent = '[刀魂][炼狱][飞瀑][劫生][北漠][割裂][活脉][恋战][愤恨][从容][蔑视][骇日]'
                    
                    
        res = re.search("^(.+)宏$", content)
        if res:
            if (res.group(1) in nickname.keys()):
                type = nickname[res.group(1)]
                trick = 0
                if type == "花间":
                    if p <= 2:
                        replycontent = '/cast 开花\n/cast [nobuff光合作用]光照\n/cast [nobuff: 开水]浇开水\n/cast [nobuff: 肥料]施肥\n/cast [buff:O2&H2O]光合作用\n/cast [buff: 开花]成熟\n/cast [buff: 成熟]吃人'
                        trick = 1
                    else:
                        replycontent = '/cast [tnobuff:兰摧玉折] 兰摧玉折\n/cast 水月无间\n/cast [tnobuff:兰摧玉折&tnobuff:钟林毓秀] 钟林毓秀\n/cast [tnobuff:商阳指] 商阳指\n/fcast 玉石俱焚\n/cast 快雪时晴'
                elif type == "奶花":
                    replycontent = '奶妈还想用宏？想多了吧'
                    trick = 1
                elif type == "冰心":
                    replycontent = '/cast 繁音急节\n/cast 剑破虚空\n/cast 玳弦急曲'
                elif type == "奶秀":
                    replycontent = '奶妈还想用宏？想多了吧'
                    trick = 1
                elif type == "毒经":
                    replycontent = '/cast 蛊虫献祭\n/cast 灵蛇引\n/fcast 幻击\n/cast 攻击\n/cast 蛊虫狂暴\n/cast 灵蛊\n/cast 百足\n/cast [tnobuff:蛇影] 蛇影\n/cast 蟾啸\n/cast 蝎心'
                elif type == "奶毒":
                    replycontent = '奶妈还想用宏？想多了吧'
                    trick = 1
                elif type == "莫问":
                    replycontent = '宏1:\n/fcast [tbufftime:角>13&tbufftime:角<15&nobuff:孤影化双&nobuff:清绝影歌] 清绝影歌\n/cast 剑·羽\n/cast 剑·宫\n宏2:\n/fcast 阳春白雪\n/cast [tnobuff:商] 商\n/cast [tnobuff:角] 角\n/fcast [tbufftime:商<6&tbufftime:商>4] 宫\n/cast 徵\n/cast 羽'
                elif type == "奶歌":
                    replycontent = '奶妈还想用宏？想多了吧'
                    trick = 1
                elif type == "剑纯":
                    replycontent = '输出：\n/cast [nobuff:碎星辰] 碎星辰\n/cast [qidian>8] 无我无剑\n/cast 八荒归元\n/cast 三环套月\n行天道辅助：\n/cast [nobuff:行天道] 生太极\n/cast [nobuff:行天道] 吞日月\n/cast 行天道'
                elif type == "气纯":
                    replycontent = '/fcast [nobuff:破苍穹] 破苍穹\n/cast [bufftime:气剑<3|nobuff:气剑] 万世不竭\n/fcast [qidian>8] 两仪化形\n/fcast 四象轮回\n/fcast 剑出鸿蒙\n/fcast 六合独尊'
                elif type == "藏剑":
                    replycontent = '重剑循环：\n/cast [buff:莺鸣&buff:夜雨] 峰插云景\n/cast [buff:夜雨] 松舍问霞\n/cast [buff:夜雨] 云飞玉皇\n/cast [rage<101] 听雷\n/cast 夕照雷峰\n轻剑：\n/cast 啸日\n/cast [rage>15&rage<50] 平湖断月\n/cast [rage>30&rage<80] 黄龙吐翠\n/cast 断潮\n/cast 听雷'
                elif type == "霸刀":
                    replycontent = '秀明尘身：\n/cast [nobuff:疏狂] 西楚悲歌\n/cast [rage<26&nobuff:逐鹿] 松烟竹雾\n/cast [rage<91&sun>64&nobuff:逐鹿] 雪絮金屏\n/cast 破釜沉舟\n/cast 雷走风切\n/cast 项王击鼎\n雪絮金屏:\n/cast 坚壁清野\n/cast [sun<41&nobuff:含风] 秀明尘身\n/cast [buff:含风>1|nobuff:含风] 醉斩白蛇\n/cast 刀啸风吟\n松烟竹雾：\n/fcast [tnobuff:闹须弥] 闹须弥\n/cast [rage>89] 秀明尘身\n/cast [sun>64] 雪絮金屏\n/cast 擒龙六斩\n/cast 逐鹰式\n/cast 控鹤式\n/cast 起凤式'
                elif type == "丐帮":
                    replycontent = '/cast [mana<0.1] 酒中仙\n/cast [mana>0.4] 龙战于野\n/cast [nobuff:龙跃于渊] 龙跃于渊\n/cast [mana>0.5] 蛟龙翻江\n/cast 亢龙有悔\n/cast 拨狗朝天\n/cast 横打双獒'
                elif type == "明尊":
                    replycontent = '/cast 心火叹\n/cast [tnobuff:戒火] 戒火斩\n/cast 净世破魔击\n/cast [moon>sun] 银月斩\n/cast [moon>sun|buff:魂·日] 幽月轮\n/cast [sun<61] 烈日斩\n/cast 赤日轮'
                elif type == "铁牢":
                    replycontent = '/cast [life<0.2] 啸如虎\n/cast [tnobuff:龙痕|tbufftime:龙痕<2] 龙牙\n/cast 灭\n/cast 龙吟\n/cast 穿云'
                elif type == "洗髓":
                    replycontent = '/cast 般若诀\n\cast 大狮子吼\n/cast [qidian>2&tbufftime:立地成佛<10|tnobuff:立地成佛] 立地成佛\n/cast [qidian>2] 韦陀献杵\n/cast 普渡四方'
                elif type == "惊羽":
                    if p<=2:
                        replycontent = '/cast 下潜\n/cast 上浮\n/cast 喷水'
                        trick = 1
                    else:
                        replycontent = '/cast [tnobuff:穿心] 穿心弩\n/cast [buff:追命无声|bufftime:侵火动旌>13] 追命箭\n/cast [buff:追命无声] 心无旁骛\n/cast 夺魄箭'
                elif type == "铁骨":
                    replycontent = '/cast 盾回\n/cast 寒啸千军\n/cast [energy<71] 盾壁\n/cast [rage>14] 盾挡\n/cast 盾压\n/cast 盾刀'
                elif type == "大师":
                    replycontent = '/cast [qidian>2] 罗汉金身\n/cast [qidian>2] 拿云式\n/cast [qidian>2] 韦陀献杵\n/cast 横扫六合\n/cast 守缺式\n/cast 普渡四方\n/cast 捕风式'
                elif type == "焚影":
                    replycontent = '/cast 净世破魔击\n/cast [sun<80] 伏明众生\n/cast [sun>79] 银月斩\n/cast [sun>79|buff:日盈&sun<60] 幽月轮\n/cast [sun<40] 烈日斩\n/cast 驱夜断愁\n/cast 赤日轮'
                elif type == "田螺":
                    replycontent = '/cast 千机变\n/cast 连弩形态\n/cast 攻击\n/cast [tnobuff:化血] 天女散花\n/cast 鬼斧神工\n/cast 心无旁骛\n/cast 天绝地灭\n/cast 暴雨梨花针\n/cast 蚀肌弹'
                elif type == "分山":
                    replycontent = '盾宏\n/cast [nobuff:血怒|buff:血怒<2] 血怒\n/cast [tbuff:流血] 盾击\n/cast 盾压\n/cast 盾猛\n/cast 盾刀\n刀宏\n/cast [nobuff:血怒|buff:血怒<2] 血怒\n/cast [tbufftime:流血>20] 闪刀\n/cast [tnobuff:流血|tbufftime:流血<6] 斩刀\n/cast 劫刀'  
                elif type == "傲血":
                    replycontent = ''
                if replycontent != '' and trick == 0:
                    replycontent = '使用前请把符号（特别是大于/小于号）改为英文的！\n' + replycontent
    db.commit()
    db.close()  
    
    if len(replycontent) > 30:
        replycontent = replycontent + '\n此条消息触发cd'
        time = int(jdata['time'])
        if app.info[jdata["group"]]['cd'] < time:
            app.info[jdata["group"]]['cd'] = max(time, app.info[jdata["group"]]['cd2']) + 120
        elif app.info[jdata["group"]]['cd2'] < time:
            app.info[jdata["group"]]['cd2'] = max(time, app.info[jdata["group"]]['cd']) + 120
        else:
            replycontent = ''
    
    if replycontent != '':
        replydata = {'reply':replycontent}
        return jsonify(replydata)
        
    return ''
    
if __name__ == '__main__':
    import signal
    
    app.info = {
      'miaomiao测试群':{'owner':['缥缈☆5.9维','眼眸印温柔','陈必过','韩景萱','无劫','长生如我-','楚🐳','Teemo','Mistletoe','  沐七。','非语','平庸的暧昧。','雨文','番茄茄茄茄茄','蛋叉蜀黍~','温粥与你立黄昏','舟舟','叶、狸','剑挽歌','大文小舍院。',], 'help':1, 'smoke':1, 'base': 'miaomiao测试群'},
      '【千衷】团本通知群':{'owner':['缥缈☆5.9维',], 'help':1, 'smoke':1, 'base': '【千衷】团本通知群'},
      '《晚枫》':{'owner':['缥缈☆5.9维',], 'help':1, 'smoke':0, 'base': '【千衷】团本通知群'},
      '【赤繁】妈耶饭里有砂':{'owner':['眼眸印温柔','陈必过'], 'help':0, 'smoke':0, 'base': '【赤繁】妈耶饭里有砂'},
      '我们的家~啾啾啾':{'owner':['韩景萱',], 'help':0, 'smoke':0, 'base': '我们的家~啾啾啾'},
      '师门炸金花':{'owner':['无劫',], 'help':0, 'smoke':0, 'base': '师门炸金花'},
      '颜值扛把子落花飞雪':{'owner':['长生如我-','The best plan'], 'help':0, 'smoke':0, 'base': '颜值扛把子落花飞雪'},
      '君不弃大型相亲现场':{'owner':['楚🐳',], 'help':0, 'smoke':0, 'base': '君不弃大型相亲现场'},
      '【烟雨阁】咸鱼养老群':{'owner':['Teemo',], 'help':0, 'smoke':0, 'base': '【烟雨阁】咸鱼养老群'},
      '【懒】弱智儿童教学班':{'owner':['Mistletoe',], 'help':0, 'smoke':0, 'base': '【懒】弱智儿童教学班'},
      '萌新基佬群':{'owner':['  沐七。',], 'help':0, 'smoke':0, 'base': '萌新基佬群'},
      '卧龙':{'owner':['非语',], 'help':0, 'smoke':0, 'base': '卧龙'},
      '浮雪老年过气团':{'owner':['平庸的暧昧。',], 'help':0, 'smoke':0, 'base': '浮雪老年过气团'},
      '高盐值咸鱼群':{'owner':['雨文',], 'help':0, 'smoke':0, 'base': '高盐值咸鱼群'},
      '团名是啥！':{'owner':['番茄茄茄茄茄',], 'help':0, 'smoke':0, 'base': '团名是啥！'},
      '女神保护基地':{'owner':['蛋叉蜀黍~',], 'help':0, 'smoke':0, 'base': '女神保护基地'},
      '青芒散尽又经年':{'owner':['温粥与你立黄昏',], 'help':0, 'smoke':0, 'base': '青芒散尽又经年'},
      '咕咕咕':{'owner':['舟舟',], 'help':0, 'smoke':0, 'base': '咕咕咕'},
      '【丫儿呦】今晚有团吗':{'owner':['叶、狸',], 'help':0, 'smoke':0, 'base': '【丫儿呦】今晚有团吗'},
      '〖天问〗加班团':{'owner':['剑挽歌',], 'help':0, 'smoke':0, 'base': '〖天问〗加班团'},
      '【春辞秋折】副本群':{'owner':['大文小舍院。',], 'help':0, 'smoke':0, 'base': '【春辞秋折】副本群'},
      '【千衷不渝养老院】':{'owner':['缥缈☆5.9维',], 'help':1, 'smoke':1, 'base': '【千衷不渝养老院】'},
      '风雨歇处既归涯':{'owner':['有风风',], 'help':0, 'smoke':0, 'base': '风雨歇处既归涯'},
      '一群小居居':{'owner':['我还能活多久',], 'help':0, 'smoke':0, 'base': '一群小居居'},
      '在剑三你甚至可以打本':{'owner':['慑、、不是射',], 'help':0, 'smoke':0, 'base': '在剑三你甚至可以打本'},
      '天天见玄晶':{'owner':['Candy',], 'help':0, 'smoke':0, 'base': '天天见玄晶'},
      '菜刀队':{'owner':['闵松月','静候轮回'], 'help':0, 'smoke':0, 'base': '菜刀队'},
      '菜刀队固定团':{'owner':['闵松月','静候轮回'], 'help':0, 'smoke':0, 'base': '菜刀队固定团'},
      '小欢乐':{'owner':['一晌贪欢'], 'help':0, 'smoke':0, 'base': '小欢乐'},
      '醉月开荒大队':{'owner':['Teemo'], 'help':0, 'smoke':0, 'base': '醉月开荒大队'},
    }
    app.overallcd = 0
    for x in app.info.keys():
        app.info[x]['cd'] = 0
        app.info[x]['cd2'] = 0
        app.info[x]['ultcd'] = 0
    app.ownGroup = {}
    app.groupLink = {}
    for group in app.info.keys():
        for owner in app.info[group]['owner']:
            if owner not in app.ownGroup.keys():
                app.ownGroup[owner] = [group,]
            else:
                app.ownGroup[owner] += [group]
        app.groupLink[group] = app.info[group]['base']
    #app.ownGroup = {'缥缈☆5.9维':['miaomiao测试群','【千衷】团本通知群','《晚枫》']}
    app.savedGroup = []
    for admin in app.ownGroup.keys():
        app.savedGroup += app.ownGroup[admin]
    updateid()
    setnickname()
    
    app.run(host='0.0.0.0', port=8888, debug=True)