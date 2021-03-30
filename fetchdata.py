from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd

# lable_url = ['小说','散文','诗歌','漫画','绘本','历史','哲学','心理学','社会学','传记','国学','摄影','职场',\
#              '养生','经济学','科普','编程','科学','管理','军事']

# def geturlall():
#     urllist = []
#     for i in range(20):
#         url_label = urlhead+lable_url[i]
#         for j in range(10):
#             # 以文学为例，爬取10个page的数据
#             pagenum = str(20*j)
#             url = url_label+'?start=' + pagenum + '&type=T'
#             urllist.append(url)
#     return urllist

urlhead = 'https://book.douban.com/tag/'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def geturl():
    lablename = input('请输入需要爬取的图书标签：')
    urllist = []
    url_label = urlhead+str(lablename)
    for j in range(10):
        pagenum = str(20*j)
        url = url_label+'?start=' + pagenum + '&type=T'
        urllist.append(url)
    # print(urllist)
    return urllist

def fetchdata(url):
    data = []
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    urltext = r.text
    #定位到正确的子标签
    soup = BeautifulSoup(urltext, 'lxml')
    soup = soup.find_all('ul')[2]
    # 获取封面
    imglist = []
    img = soup.find_all('img')
    for i in range(20):
        src = img[i].get('src')
        imglist.append(src)
    data.append(imglist)
    # print(src)
    # 获取标题
    titles = []
    for title in soup.find_all('a'):
        title = title.get('title')
        if title != None:
            titles.append(title)
    data.append(titles)
    # print(titles)
    # 获取作者
    pubinfo = []
    for info in soup.find_all('div','pub'):
        pubinfo.append(info.string)
    data.append(pubinfo)
    # print(pubinfo)
    # 获取评分
    ratelist = []
    for rate in soup.find_all('span','rating_nums'):
        ratelist.append(rate.string)
    data.append(ratelist)
    # print(ratelist)
    # #获取评价人数
    ratenum = []
    for num in soup.find_all('span','pl'):
        ratenum.append(num.string)
    data.append(ratenum)
    # print(ratenum)
    data = pd.DataFrame(data)
    data = data.T
    # print(data)
    return data

def savecsv():
    filename = input('请输入文件名：')
    csvheaders = ['封面', '标题', '出版信息', '评分', '评价人数']
    with open(filename,'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(csvheaders)
        for j in range(len(datas)):
            rows = datas[j].values.tolist()
            f_csv.writerows(rows)

if __name__ == '__main__':
    datas = []
    url = geturl()
    for i in range(10):
        datas.append(fetchdata(url[i]))
    # print(datas)
    savecsv()





























