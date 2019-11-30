# import pickle
#
# with open("山西大学课程信息.txt","rb") as f:
#     data = pickle.load(f)

import requests
import time
import random
import pymysql


#连接数据库
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',password='123456',
    database='sxlesson',
    charset='utf8')


# 获取cookie
url1 = "http://bkjw.sxu.edu.cn/ZNPK/KBFB_LessonSel.aspx"
res = requests.get(url1)

# 获取验证码

url2 = 'http://bkjw.sxu.edu.cn/sys/ValidateCode.aspx'
r2 = requests.get(url2,headers={
    'Host':'bkjw.sxu.edu.cn',
    'Referer':'http://bkjw.sxu.edu.cn/ZNPK/KBFB_LessonSel.aspx'
})

# 获取验证码图片
con = r2.content[0:r2.content.index("\r\n\r\n".encode())]
with open("yzm.png","wb") as f:
    f.write(con)

yzm = input("请输入验证码:\n")

def getTable(xnxq,kc):
    """
    :param xnxq:  学年学期ID
    :param kc: 课程id
    :return:
    """
    time.sleep(random.randint(0,3))
    url3 = "http://bkjw.sxu.edu.cn/ZNPK/KBFB_LessonSel_rpt.aspx"
    res3 = requests.post(url3,data={
        'Sel_XNXQ':xnxq,
        'Sel_KC':kc,
        'gs':'1',
        'txt_yzm':yzm,
    },cookies=r2.cookies,headers={
        'Host':'bkjw.sxu.edu.cn',
        'Referer':'http://bkjw.sxu.edu.cn/ZNPK/KBFB_LessonSel.aspx'
    })
    from lxml import etree
    html = etree.HTML(res3.text)
    table = html.xpath("//div[@id='pageRpt']")[0]
    con = etree.tostring(table,encoding="utf8")
    cursor = conn.cursor()
    sql = "insert into lessondata (xnxq,lesson,con) values (%s,%s,'%s')"%(xnxq,kc,con.decode())
    cursor.execute(sql)
    conn.commit()

import pickle
with open('sxLessonData.txt',"rb") as f:
    data = pickle.load(f)

for item in data:
    xnxq = item['code']
    print("正在爬取 %s"%item['title'])
    for obj in item['lesson']:
        print("正在爬取 %s"%obj['title'])
        kc = obj['code']
        try:
            getTable(xnxq,kc)
        except:
            print("%s %s数据异常"%(item['title'],obj['title']))




