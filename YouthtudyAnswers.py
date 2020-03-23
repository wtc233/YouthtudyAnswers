# -*- coding: utf-8 -*-
#Author:    mlge
#Time:      2020/3/23 10:11
#Version:   v1.05


import codecs
import time
import requests
from lxml import html
import re
import sys


if len(sys.argv) > 1:
    if sys.argv[1] == "last":
        last = 1
    else:
        last = 0
else:
    last = 0
def getMidString(str, start_str, end_str):
    start = str.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = str.find(end_str, start)
        if end >= 0:
            return str[start:end].strip()

response = requests.get(
    "http://h5.cyol.com/special/daxuexi/daxuexiall/am.html",
    headers={
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2526 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Host": "h5.cyol.com",
        "Accept-Encoding": "gzip, deflate, br"
    }
)
response.encoding = 'utf-8'
lastUrl = re.findall(r"\$\('#[\s\S]*? \.[\s\S]*?'\)\.click\(function\(\){[\s]*location.href='([\s\S]*?)';[\s]*}\);", response.text)[-1]
print(lastUrl)

response = requests.get(
    lastUrl,
    headers={
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2526 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Host": "h5.cyol.com",
        "Accept-Encoding": "gzip, deflate, br"
    }
)
response.encoding = 'utf-8'
lastUrl = re.findall(r"\$\('#[\s\S]*? \.[\s\S]*?'\)\.click\(function\(\){[\s]*location.href='([\s\S]*?)';[\s]*}\);", response.text)[-1].replace("index.php", "m.php").replace("index.htm", "m.htm")
if last == 1:
    base = {
        "q": "w",
        "w": "e",
        "e": "r",
        "r": "t",
        "t": "y",
        "y": "u",
        "u": "i",
        "i": "o",
        "o": "p",
    }
    regex = re.findall("""([\s\S]*?)(daxuexi)([1-9][0-9]*)([qwertyuiop])([1-9][0-9]*)([\s\S]*)""", lastUrl)[0]
    lastUrl = regex[0] + regex[1] + regex[2] + base[regex[3]] + str(int(regex[4]) + 1) + regex[5]
print(lastUrl)

response = requests.get(
    lastUrl,
    headers={
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2526 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Host": "h5.cyol.com",
        "Accept-Encoding": "gzip, deflate, br"
    }
)
if(response.status_code == 404):
    print("官方未创建最新一期")
    sys.exit(0)
response.encoding = 'utf-8'
title = getMidString(response.text, "var shareDesc = '", "';")
miniTitle = getMidString(response.text, "var shareTitle = '", "';")
publishDate = html.fromstring(response.text).xpath("//meta[@name='publishdate']/@content")[0]
titleImg = getMidString(response.text, "var shareImg = '", "';")
video = html.fromstring(response.text).xpath("//video[@id='Bvideo']/@src")[0]
print(miniTitle + "——《" + title + "》[" + publishDate + "]")
print(titleImg)
print(video)

answers = {}
orders = {}

regex = re.finditer("""<div class=['"](\S+)['"]>\s*(<div class=['"]\S+['"]></div>\s*)*(<div class=['"]\S+['"] data-a=['"]\S['"][\s\S]*?></div>\s*)+(<div class=['"]\S+['"]></div>\s*)*</div>""", response.text)
for i in regex:
    regexS = re.findall("""<div class=['"]\S+['"] data-a=['"](\S)['"][\s\S]*?></div>""", i.group())
    base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    answer = ""
    for j in range(0, len(regexS)):
        if regexS[j] == '1':
            answer += base[j]
    answers[i.groups()[0]] = [answer]
    orders[i.start()] = i.groups()[0]

regex = re.finditer("""<div class=['"](\S+)['"]>\s*(<div class=['"]\S+['"]></div>\s*)*<div class=['"]\S+_ul['"]>\s*(<div class=['"]\S+_li['"] data=['"]\S+['"] data1=-2></div>\s*)+</div>\s*(<div class=['"]\S+['"]></div>\s*)*</div>""", response.text)
for i in regex:
    rightAnswer = getMidString(getMidString(response.text, """$(".""" + i.groups()[0] + """_click").on('click',function(){""", "});"), "if(", "){")
    regexS = re.findall("""data1.ary2\[\S\]==(\S)""", rightAnswer)
    base = "①②③④⑤⑥⑦⑧⑨⑩"
    answer = ""
    for j in range(0, len(regexS)):
        answer += base[int(regexS[j])]
    answers[i.groups()[0]] = [answer]
    orders[i.start()] = i.groups()[0]

questionAfterClass = getMidString(getMidString(response.text, "$('.section3 .w0').on('click',function(){", "});"), "$('", "').removeClass('topindex1');").replace(".", "").split(",")

ordersNew = {}
for i in sorted(orders.keys()):
    ordersNew[i] = orders[i]
n = len(ordersNew)
y = len(questionAfterClass)
x = n - y
answersString = ""
for i in range(0, x):
    tmp = "第" + str(i + 1) + "题：" + answers[ordersNew[list(ordersNew.keys())[i]]][0]
    answersString += tmp + "<br />"
    print(tmp)
for i in range(0, y):
    tmp = "课后第" + str(i + 1) + "题：" + answers[ordersNew[list(ordersNew.keys())[i + x]]][0]
    answersString += tmp + "<br />"
    print(tmp)

resultHTML = """
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8" />
        <title>青学Answers</title>
        <meta itemprop="name" content="青学Answers" />
        <meta itemprop="image" content="splittitleImg" />
        <meta name="description" itemprop="description" content="辣鸡业余开发者写的辣鸡网页，用于自动获取坠新的青年大学习答案。" />
        <link rel="shortcut icon" href="https://www.mlge.xyz/wp-content/uploads/2019/11/cropped-HEART%E5%93%88%E5%A3%AB%E5%A5%87-32x32.png"/>
        <link rel="icon" href="https://www.mlge.xyz/wp-content/uploads/2019/11/cropped-HEART%E5%93%88%E5%A3%AB%E5%A5%87-32x32.png" sizes="32x32" />
        <link rel="icon" href="https://www.mlge.xyz/wp-content/uploads/2019/11/cropped-HEART%E5%93%88%E5%A3%AB%E5%A5%87-192x192.png" sizes="192x192" />
        <link rel="apple-touch-icon-precomposed" href="https://www.mlge.xyz/wp-content/uploads/2019/11/cropped-HEART%E5%93%88%E5%A3%AB%E5%A5%87-180x180.png" />
        <meta name="msapplication-TileImage" content="https://www.mlge.xyz/wp-content/uploads/2019/11/cropped-HEART%E5%93%88%E5%A3%AB%E5%A5%87-270x270.png" />
    </head>
    <body style="text-align: center">
        <a href="splitvideo"><img style="width: 300px; height: 300px" src="splittitleImg" /></a>
        <h1>《splittitle》</h1>
        <h3>splitminiTitle</h3>
        <h5>官方编辑日期：splitpublishDate</h5>
        <p>splitanswersString</p>
        <a href="./last.html">这是坠新的已公开显示的一期，如需偷跑未公开显示的一期请点击本行</a><br />
        Copyright © 青学Answers by <a href="https://www.mlge.xyz">mlge</a> All Rights Reserved.<br />
        Powered by Python 3.8.2<br />
        Source Code: <a href="#">YouthtudyAnswers - Github(暂未上传)</a><br />
        Update Time: splitupdateTime
    </body>
</html>
"""
updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
resultHTML = resultHTML.replace("splittitleImg", titleImg).replace("splittitle", title).replace("splitminiTitle", miniTitle).replace("splitpublishDate", publishDate).replace("splitvideo", video).replace("splitanswersString", answersString).replace("splitupdateTime", updateTime)
if last == 1:
    resultHTML = resultHTML.replace(r'<a href="./last.html">这是坠新的已公开显示的一期，如需偷跑未公开显示的一期请点击本行</a><br />', r'<a href="./index.html">这是坠新的未公开显示的一期，如需返回已公开显示的一期请点击本行</a><br />')
if last == 0:
    file = codecs.open("index.html", "w", "utf-8")
elif last == 1:
    file = codecs.open("last.html", "w", "utf-8")
file.write(resultHTML)
