
# coding: utf-8

# In[1]:

#!/usr/bin/python3

#获取时间，标题，链接
#requests取得HTML内容
import requests   
from bs4 import BeautifulSoup      
import pymysql

#打开数据库链接
#######一定要加上charset='utf8'，少了这个东西被它困扰了两天
conn = pymysql.connect("localhost",'root','','sinanews',charset='utf8')
#使用 execute() 方法创建一个游标对象 cur
cur = conn.cursor()
#使用 execute() 方法执行 SQL 查询
cur.execute('SELECT VERSION()')

res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
#print(res.text)
#接下来要用到BeautifulSoup4包
#在bs4套件中读入BeautifulSoup方法
#将网页读进BeautifulSoup中：BeautifulSoup(res.text)
#指示剖析器为'html.parser'，否则会使用默认剖析器而出现警告 
soup = BeautifulSoup(res.text,'html.parser')
#使用BeautifulSoup4找出class = news-item的元素 
id = 0
for news in soup.select('.news-item'): 
    if(len(news.select('h2'))>0):
        name = str(news.select('h2')[0].text)
        time = str(news.select('.time')[0].text)
        href = str(news.select('a')[0]['href'])
        #插入语句
        sql = "insert into newsurl(id, name, time, href) values(%d,'%s','%s','%s')" %                (id, name, time, href)
             
        try:
            #执行sql语句
            cur.execute(sql)
            #提交到数据库执行
            conn.commit()
            #print(id, name, time, href)
        except:
            # 发生错误时回滚
            conn.rollback()
            
        id = int(id + 1)

#关闭数据库
cur.close()
conn.close()


# In[2]:

#获取总评论数
import re
import json
#网页链接
#newsurl = 'http://news.sina.com.cn/c/nd/2017-07-03/doc-ifyhrxsk1622226.shtml'
#评论链接模板
commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
def getCommentCounts(newsurl):
    #也可以使用正则表达式，使用re套件,获取userid
    #import re
    m = re.search('doc-i(.*).shtml',newsurl)
    userid = m.group(1)
    #把userid补入模板，得到评论链接
    #requests读取网页内容
    comments = requests.get(commentURL.format(userid))
    #使用json套件.获得总评论数
    #import json
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']


# In[10]:

import requests
from bs4 import BeautifulSoup
from datetime import datetime



#新闻内容
def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text
    timesource = soup.select('.time-source')[0].contents[0].strip()
    result['dt'] = datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
    result['newssource'] = soup.select('.time-source span a')[0].text
    result['article'] =  ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['editor'] = soup.select('.article-editor')[0].text.lstrip('责任编辑：')
    result['comment'] = getCommentCounts(newsurl)
    return result


# In[ ]:

import requests   
from bs4 import BeautifulSoup      
import pymysql
from datetime import datetime
import time

#获取总评论数
import re
import json
#网页链接
#newsurl = 'http://news.sina.com.cn/c/nd/2017-07-03/doc-ifyhrxsk1622226.shtml'
#评论链接模板
commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
def getCommentCounts(newsurl):
    #也可以使用正则表达式，使用re套件,获取userid
    #import re
    m = re.search('doc-i(.*).shtml',newsurl)
    userid = m.group(1)
    #把userid补入模板，得到评论链接
    #requests读取网页内容
    comments = requests.get(commentURL.format(userid))
    #使用json套件.获得总评论数
    #import json
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']

#打开数据库链接
#######一定要加上charset='utf8'，少了这个东西被它困扰了两天
conn = pymysql.connect("localhost",'root','','sinanews',charset='utf8')
#使用 execute() 方法创建一个游标对象 cur
cur = conn.cursor()
#使用 execute() 方法执行 SQL 查询
cur.execute('SELECT VERSION()')


#提取数据库href值
sql = "select * from newsurl"
try:
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        #赋值给newsurl
        newsurl = row[3]
        
        time.sleep(500)
        #运行新闻提取函数
        res = requests.get(newsurl)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,'html.parser')
        time.sleep(500)
        title = soup.select('#artibodyTitle')[0].text
        timesource = soup.select('.time-source')[0].contents[0].strip()
        dt = datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
        newssource = soup.select('.time-source span')[0].text.strip()
        article =  ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
        editor = soup.select('.article-editor')[0].text.lstrip('责任编辑：')
        comment = getCommentCounts(newsurl)
        print (comment)
        #sql插入语句
        #运行sql语句
        #提交到数据库执行
        #发生错误时回滚
except:
    print ("Error: unable to fetch data")
        
#关闭数据库
cur.close()
conn.close()


# In[ ]:



