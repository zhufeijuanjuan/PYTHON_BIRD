# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re


def getHTMLText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding="utf-8"
        return r.text
    except:
        return""

def Getinfo(Infolist,moviepage):
    soup = BeautifulSoup(moviepage, 'html.parser')
    movielist = soup('ol')[0]
    for movie in movielist('li'):
        title=movie("span",class_="title")[0].string
        try:
            rating = movie('span', class_='rating_num')[0].string
        except IndexError:
            rating = '无评分'
        try:
            comments = movie('span', class_='inq')[0].string
        except IndexError:
            comments = '无评论'
        Infolist.append([title,rating,comments])


def printlist(Infolist):
    tplt = "{:^4}\t{:^32}\t{:^20}\t{:^50}"
    print(tplt.format("序号", "电影名字", "评分","影评"))
    count = 0
    for g in Infolist:
        count += 1
        print(tplt.format(count, g[0], g[1], g[2]))

def saveInfo(Infolist):
    filename="douban.txt"
    with open(filename,"w")as f:
        tplt = "{:^4}\t{:^32}\t{:^20}\t{:^50}\n"
        count = 0
        for g in Infolist:
            count += 1
            f.write(tplt.format(count, g[0], g[1], g[2]))


def main():
    start_url="https://movie.douban.com/top250?"
    depth=5
    infolist = []
    for page in range(depth):
        try:
            url=start_url+"start="+str(25*page)+ '&filter='
            moviepage = getHTMLText(url)
            Getinfo(infolist,moviepage)
        except:
            print("爬取失败")
        printlist(infolist)
        saveInfo(infolist)

main()
