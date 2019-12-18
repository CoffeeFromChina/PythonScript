import re
import requests
import time
import pprint
from os import path

# 爬取 https://www.gushiwen.org/ 诗词


HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


def spider_page(url):
    response = requests.get(url, headers=HEADERS)
    text_raw = response.text

    titles = re.findall(r'<div\sclass="cont">.*?<p>.*?<b>(.*?)</b>.*?</p>', text_raw, re.DOTALL)        # 题目

    eras = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>', text_raw, re.DOTALL)                    # 朝代

    contsons_pre = re.findall(r'<div\sclass="contson"\s.*?>(.*?)</div>', text_raw, re.DOTALL)           # 内容

    authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?</a>.*?<a.*?>(.*?)</a>', text_raw, re.DOTALL)

    Types_pre =  re.findall(r'<div\sclass="tag">(.*?)</div>', text_raw, re.DOTALL)                      # 诗歌类别（先获取<div class="tag"> 下的内容，再清洗数据 ）

    # 清洗诗歌类别信息
    Types = []
    for tt in Types_pre:
        a = re.sub(r'<span>.*?</span>|<a.*?>|</a>|',"",tt)  # 清洗数据
        b = a.replace('\n', ' ')                            # 用逗号替换 '\n'
        b = b.strip()                                       # 清除首位空格
        Types.append(b)                                     # 添加到列表中


    contsons = []
    for contson in contsons_pre:                                                                    # 去除内容杂质
        c = re.sub(r'\n|<.*?>', '', contson)
        contsons.append(c)

    poems=[]
    for value in zip(contsons,Types, eras, authors,titles):
        contson,Type, era , author, title = value
        poem={
            'title': title,
            'author': author,
            'contson': contson,
            'era': era,
            'Type':Type
        }

        poems.append(poem)
    return poems


def spider():
    poems = []

    for page_num in range(10):
        url='https://www.gushiwen.org/default_{}.aspx'.format(page_num)

        print('开始爬取第{}页诗词数据'.format(page_num+1))
        
        poems.append(spider_page(url))

        time.sleep(1)

    for poem in poems:
        pprint.pprint(poem)
        print("==" * 40)

if __name__ == '__main__':
    spider()