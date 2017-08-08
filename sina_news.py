
# coding: utf-8

# In[3]:

#获取时间，标题，链接
#requests取得HTML内容
import requests
res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
#print(res.text)
#接下来要用到BeautifulSoup4包
#在bs4套件中读入BeautifulSoup方法 
from bs4 import BeautifulSoup
#将网页读进BeautifulSoup中：BeautifulSoup(res.text)
#指示剖析器为'html.parser'，否则会使用默认剖析器而出现警告 
soup = BeautifulSoup(res.text,'html.parser')
#使用BeautifulSoup4找出class = news-item的元素 
for news in soup.select('.news-item'): 
    if(len(news.select('h2'))>0):
        h2 = news.select('h2')[0].text
        time = news.select('.time')[0].text
        a = news.select('a')[0]['href']
    #print(time,h2,a)


# In[4]:

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


# In[19]:

import requests
from bs4 import BeautifulSoup
from datetime import datetime

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


# In[20]:

newsurl = 'http://news.sina.com.cn/c/nd/2017-07-03/doc-ifyhrxsk1622226.shtml'
getNewsDetail(newsurl)

