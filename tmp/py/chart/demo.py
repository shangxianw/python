#!/usr/bin/python3

#@Readme : IP代理==模拟一个ip地址去访问某个网站（爬的次数太多，ip被屏蔽）

# 多线程的方式构造ip代理池。
from bs4 import BeautifulSoup
import requests
from urllib import request, error
import threading

import os
from fake_useragent import UserAgent


inFile = open('proxy.txt')           # 存放爬虫下来的ip
verifiedtxt = open('verified.txt')   # 存放已证实的可用的ip

lock = threading.Lock()

def getProxy(url):
    # 打开我们创建的txt文件
    proxyFile = open('proxy.txt', 'a')

    # 伪装
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    # page是我们需要获取多少页的ip，这里我们获取到第９页
    for page in range(1, 2):
        # 通过观察ＵＲＬ，我们发现原网址+页码就是我们需要的网址了，这里的page需要转换成str类型
        urls = url + str(page)
        # 通过requests来获取网页源码
        rsp = requests.get(urls, headers=headers)
        html = rsp.text
        # 通过BeautifulSoup，来解析html页面
        soup = BeautifulSoup(html,'html.parser')
        # 通过分析我们发现数据在　id为ip_list的table标签中的tr标签中
        trs = soup.find('table', id='ip_list').find_all('tr')  # 这里获得的是一个list列表
        # 我们循环这个列表
        for item in trs[1:]:
            # 并至少出每个tr中的所有td标签
            tds = item.find_all('td')
            # 我们会发现有些img标签里面是空的，所以这里我们需要加一个判断
            if tds[0].find('img') is None:
                nation = '未知'
                locate = '未知'
            else:
                nation = tds[0].find('img')['alt'].strip()
                locate = tds[3].text.strip()
            # 通过td列表里面的数据，我们分别把它们提取出来
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            anony = tds[4].text.strip()
            protocol = tds[5].text.strip()
            speed = tds[6].find('div')['title'].strip()
            time = tds[8].text.strip()
            # 将获取到的数据按照规定格式写入txt文本中，这样方便我们获取
            proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol, speed, time))


def verifyProxyList():
    verifiedFile = open('verified.txt', 'a')

    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        ip = line[1]
        port = line[2]
        realip = ip + ':' + port
        code = verifyProxy(realip)
        if code == 200:
            lock.acquire()
            print("---Success成功:" + ip + ":" + port)
            verifiedFile.write(ll + "\n")
            lock.release()
        else:
            print("---Failure失败:" + ip + ":" + port)


def verifyProxy(ip):
    '''
    验证代理的有效性
    '''
    ua = UserAgent()
    requestHeader = {
        'User-Agent': ua.random
    }
    url = "https://blog.csdn.net"
    # 填写代理地址
    proxy = {'http': ip}
    # 创建proxyHandler
    proxy_handler = request.ProxyHandler(proxy)
    # 创建ｏｐｅｎｅｒ
    proxy_opener = request.build_opener(proxy_handler)
    # 安装opener
    request.install_opener(proxy_opener)

    try:
        req = request.Request(url, headers=requestHeader)
        rsq = request.urlopen(req, timeout=5.0)
        code = rsq.getcode()
        return code
    except error.URLError as e:
        return e


if __name__ == '__main__':
    # 手动新建两个文件
    filename = 'proxy.txt'
    filename2 = 'verified.txt'
    if not os.path.isfile(filename):
        inFile = open(filename, mode="w", encoding="utf-8")
    if not os.path.isfile(filename2):
        verifiedtxt = open(filename2, mode="w", encoding="utf-8")
    tmp = open('proxy.txt', 'w')
    tmp.write("")
    tmp.close()
    tmp1 = open('verified.txt', 'w')
    tmp1.write("")
    tmp1.close()
    # 多线程爬虫西刺代理网，找可用ip
    getProxy("http://www.xicidaili.com/nn/")
    getProxy("http://www.xicidaili.com/nt/")
    getProxy("http://www.xicidaili.com/wn/")
    getProxy("http://www.xicidaili.com/wt/")

    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()

    inFile.close(param)
    verifiedtxt.close()