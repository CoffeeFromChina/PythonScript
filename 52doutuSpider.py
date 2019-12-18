import requests
import re
import os
import time
from os import path
import urllib.request as ur

HEADERS = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

picture = dict()    # 存放图片信息
fileSize = 0        # 统计图片大小


def downImg():
    global fileSize
    os.chdir('F:\\52doutu')                                 # 更改工作目录
    for key in picture:
        fileName = key.replace('?', '问号')                 # 去除问号
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")    # 匹配不是中文、大小写、数字的其他字符
        fileName = cop.sub('', fileName)                    #将fileName中匹配到的字符替换成空字符

        if (path.exists(picture[key])):                     # 判断文件是否以下载
            continue

        fileType = path.splitext(picture[key])[-1]          # 获取文件类型，-1：文件后缀。0：文件名
        # 判断文件类型，并存储为相应类型的文件
        if (fileType == '.jpg'):
            print("正在下载-->{}".format(fileName + '.jpg'))
            ur.urlretrieve(picture[key],
                           filename=fileName + '.jpg')      # 下载图片。直接以图片原名命名
        elif fileType == '.png':
            print("正在下载-->{}".format(fileName + '.png'))
            ur.urlretrieve(picture[key], filename=fileName + '.png')
        else:
            print("正在下载-->{}".format(fileName + '.gif'))
            ur.urlretrieve(picture[key], filename=fileName + '.gif')

        fileSize = fileSize + path.getsize(                 # 获取文件大小
            'F:\\52doutu\\{}'.format(fileName + fileType))
    time.sleep(5)                                           # 下载完成后，程序暂停5秒

    print("以抓取完毕，共计{}MB".format(fileSize / float(1024 * 1024)))


def spider():
    start = time.time()
    for num in range(1, 11000, 100):                        # 分批次下载图片，100 张一批
        for j in range(0, 100, 1):
            url = 'https://www.52doutu.cn/i/{}/'.format(num + j)
            response = requests.get(url, headers=HEADERS)
            txt = response.text                             # 获取页面信息

            # 正则表达式匹配页面元素
            title = re.findall(r'<h2 class="left-main-title">(.*?)</h2>', txt,
                               re.DOTALL)
            link = re.findall(
                r'<img class="lazyload img-responsive".*?data-original="(.*?)".*?>',
                txt, re.DOTALL)

            print("正在抓取第{}张图片-->{}".format(num + j, title))

            picture.update(zip(title, link))
        time.sleep(4)                                       # 每爬取100张，程序暂停4秒
        downImg()
    end = time.time()
    print("抓取图片攻击耗时{}秒".format(end - start))

if __name__ == "__main__":
    spider()