import requests
from lxml import etree

# 获取山西大学2015-2020学年 课程信息
url1 = url = "http://bkjw.sxu.edu.cn/ZNPK/KBFB_LessonSel.aspx"

# 获取学年 课程
url2 = 'http://bkjw.sxu.edu.cn/ZNPK/Private/List_XNXQKC.aspx?xnxq=20190'

response = requests.get(url)
html = etree.HTML(response.text)
xnxq = html.xpath("//select[@name='Sel_XNXQ']/option/text()")
xnxqId = html.xpath("//select[@name='Sel_XNXQ']/option/@value")
# 学期课程
lessonData = []


# 获取学年学期课程内容
def get_lesson(xnxqid):
    response = requests.get(url2)
    html = etree.HTML(response.text)
    res = html.xpath("//script/text()")
    html2 = etree.HTML(res[0][23:-1])
    res1 = html2.xpath("//option/text()")
    res2 = html2.xpath("//option/@value")
    lesson = []
    for code,title in zip(res2,res1[1:],):
        lesson.append({'code':code,'title':title})
    return lesson


# 学年学期
for code,title in zip(xnxqId,xnxq):
    obj = {'code':code,'title':title,'lesson':get_lesson(code)}
    lessonData.append(obj)

# 保存到 文件
import pickle

with open('sxLessonData.txt','wb+') as f:
    pickle.dump(lessonData,f)


"""
lessonData = [
    {
        'code':'学期学号ID',
        'title':'学期标题',
        'lesson':[
            {
                'code':'课程ID',
                'title':'课程名称'
            }
        ]
    }
]
"""