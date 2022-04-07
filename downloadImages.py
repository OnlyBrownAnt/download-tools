import requests
import re
from bs4 import BeautifulSoup
import os

def getResource(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    response = requests.get(url, headers = headers, verify = False)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response
    return None

def download(list, url, homePath): 
    for i in range(len(list)):
        print("开始下载图片：" + list[i] + "\r\n")
        try:
            pic = requests.get(list[i], timeout = 10)
        except requests.exceptions.ConnectionError:
            print("图片无法下载")
            continue

        imgPath = homePath + os.sep + re.split(url, list[i])[1]
        imgPath = imgPath.replace("/", os.sep)
        imgPathList = re.split(os.sep, imgPath)
        imgPathList.reverse()
        imgDir = re.sub(imgPathList[0], "", imgPath)
        if os.path.exists(imgDir) == False:
            print("该文件夹不存在")
            os.makedirs(imgDir)
            print("已创建文件夹")
        fp = open(imgPath, 'wb')
        fp.write(pic.content)
        fp.close()
        print("图片下载结束！" + "\r\n")
   
def getImgAddressList(html, url):
    list = re.findall("src.*=.*'.*'", html)
    for i in range(len(list)):
        list2 = re.split("'", list[i])
        list[i] = url + list2[1]
    return list

# 预设绝对路径 当前路径/imgs
def getHomePath():
    dirPath = os.path.abspath('imgs')
    if os.path.exists("imgs"):
        return dirPath
    os.mkdir(dirPath)
    return dirPath + os.sep

def downloadImgsByUrl(imgUrl):
    response = getResource(imgUrl)
    if response == None:
        return False
    html = response.text
    imgList = getImgAddressList(html, imgUrl)
    homePath = getHomePath()
    download(imgList, imgUrl, homePath)

if __name__ == '__main__':
    mainPage = 'https://lee-7723.github.io/Veibae-Emoji/'
    downloadImgsByUrl(mainPage)