#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
import re
from BeautifulSoup import BeautifulSoup
import sqlite3

ID = 1
searchnumber = 1

def scrapeLinks(baseUrl,data):
    soup = BeautifulSoup(data)
    links=[]
    for anchor in soup.body.findAll('a',target="_blank",rel="nofollow"):
        links.append(str(anchor['href']))
    return links
def rmRepeat(links):
    check=[]
    for e in links:
        if e not in check:
            check.append(e)

    return check

def scrapeContents(data):
    soup = BeautifulSoup(data)
    name = soup.findAll('h1')[0].string
    print name
    print type(name)
    region = ""
    for item in re.findall(r"【(.*?)】",str(name)):
        region = item
    print region
    print type(region)

    price = 0
    temp = soup.findAll('p',attrs={"class":"deal-price"})
    for item in re.findall(r"[0-9]+\.?[0-9]*",str(temp[0].contents[1].string)):
        price = float(item)
    print "团购价格: "+str(price)


    originalPrice = 0
    temp = soup.findAll(attrs={"class":"deal-discount"})
    for item in re.findall(r"[0-9]+\.?[0-9]*",str(temp[0].contents[3].contents[1].contents[0].string)):
        originalPrice = float(item)
    print  "原始价格: "+str(originalPrice)
    print type(originalPrice)

    discount = 0
    for item in re.findall(r"[0-9]+\.?[0-9]*",str(temp[0].contents[3].contents[3].contents[0].string)):
        discount = float(item)
    print discount   

    saveMoney = 0
    for item in re.findall(r"[0-9]+\.?[0-9]*",str(temp[0].contents[3].contents[5].contents[0].string)): 
        saveMoney = float(item)
    print "saveMoney: "+str(saveMoney)
    print type(saveMoney)

    
    soldout = 0 #mei mai wan
    temp = soup.findAll(attrs={"class":"deal-buy-tip-top"})
    #print temp[0]
    if len(temp) != 0:
        if len(temp[0].contents)==1:
            soldNumber = 0
        else:
            soldNumber = int(temp[0].contents[0].contents[0])
    else:
        temp = soup.findAll(attrs={"class":"deal-buy-tip-total"})
        soldout = 1
        soldNumber = int(temp[0].contents[1].contents[0])
    print "soldNumber: "+str(soldNumber)

    sevenOrNot = -1 #this group has no this selection
    expireOrNot = -1
    temp=soup.findAll(attrs={"class":"seven"})
    temp2=soup.findAll(attrs={"class":"expire"})
    if len(temp)==0:
        temp=soup.findAll(attrs={"class":"no-seven"})
        temp2=soup.findAll(attrs={"class":"no-expire"})
    if len(temp) != 0:
        s=temp[0].contents[1].contents[0].contents[0][0]
        print s
        if s==u'\u652f':
            sevenOrNot = 1
        elif s==u'\u4e0d':
            sevenOrNot = 0

        s=temp2[0].contents[1].contents[0].contents[0][0]
        print s
        if s==u'\u652f':
            expireOrNot = 1
        elif s==u'\u4e0d':
            expireOrNot = 0
    elif len(temp) == 0:
        temp = soup.findAll(attrs={"class":"deal-commitment"})
        if len(temp) != 0:
            s = temp[0].contents[1].contents[0][0]
            print s
            if s == u'\u652f':
                sevenOrNot = 1
            elif s == u'\u4e0d':
                sevenOrNot =0
            print "#",
            s = temp[0].contents[3].contents[0][0]
            print s
            if s == u'\u652f':
                expireOrNot = 1
            elif s == u'\u4e0d':
                expireOrNot = 0
                

     
# 不同商品页面关于此内容的标签不一样,将问题放在此，日后再想解决办法
#    temp = soup.findAll(attrs={"class":"no-seven"})
    #ss = temp[0].contents[1].contents[0].string
    #ss = str(ss)
    #if ss[0] == '\xe4':
    #    sevenOrNot = 0
    #else:
    #    sevenOrNot = 1
    #print sevenOrNot

    validStartTime="no data"
    validEndTime="no data"
    temp = soup.findAll(attrs={"class":"col first"})
    m=str(temp[0].contents[3].contents[1].string)
    day = re.findall(r"[0-9]+.[0-9]+.[0-9]+",m)
    if len(day)!=0:
        validStartTime = day[0]
        validEndTime = day[1]

    print validStartTime
    print validEndTime
    tips = []
    #tips.append(temp[0].contents[3].contents[1].string)
    #tips.append(temp[0].contents[3].contents[2].string)
    #tips.append(temp[0].contents[3].contents[4].string)
    #tips.append(temp[0].contents[3].contents[6].string)
    #tips.append(temp[0].contents[3].contents[8].string)
    for content in temp[0].contents[3].contents:
        if str(content.string) != "\n" and content.string != None:
            print content.string
            tips.append(content.string)
    print "tips:"
    for i in tips:
        print i
    strtips = ','.join(tips)
    strtips = strtips.encode('utf8')
    print type(strtips)
    print strtips

    temp = soup.findAll(attrs={"class":"col"})
    greatness = []
    for content in temp[0].contents[3]:
        if str(content.string) != "\n" and content.string != None:
            greatness.append(content.string)
    print "greatness:"
    for i in greatness:
        print i
    strgreatness = ','.join(greatness)
    strgreatness = strgreatness.encode('utf8')
    print type(strgreatness)

    temp = soup.findAll(attrs={"class":"deal-buy-cover-img"})
    s = str(temp[0].contents[0])
    mainImage = re.findall(r"[a-zA-z]+://[^\s]*",s)
    mainImage = mainImage[0]
    mainImage = mainImage[:len(mainImage)-1]

    print mainImage

    #格式极为不规范，很难用通用方法抓取。。
    #servicePhone="no data"
    #temp = soup.findAll(attrs={"id":"side-business"})
    #if len(temp) != 0:
       # servicePhone = temp[0].contents[1].contents[1].contents[0]
    #print servicePhone



    print ""

    conn = sqlite3.connect('meituan.db')
    c = conn.cursor()
    """c.execute("insert into stocks(searchnumber,id,name,region,price,originalPrice,discount,saveMoney,soldNumber,sevenOrNot,expireOrNot,validStartTime,validEndTime,tips,greatness,mainImage)\
    values('%d', '%d', '%s', '%s', '%f', '%f', '%f',\
    '%f', '%d', '%d', '%d', '%s', '%s', '%s', '%s', '%s')" % (searchnumber,ID,name,region,price,originalPrice,discount,saveMoney,soldNumber,sevenOrNot,expireOrNot,validStartTime,validEndTime,strtips,strgreatness,mainImage))"""
    c.execute("insert into stocks(searchnumber,id,region,name) values('%d','%d','%s','%s')" % (searchnumber,ID,region,name))
    #c.execute("insert into stocks(id) values('%d')" % ID)
    #c.execute("insert into stocks(name) values('%s')" % name)
    #c.execute("insert into stocks(region) values('%s')" % region)
    #c.execute("insert into stocks(price) values('%f')" % price)
    #c.execute("insert into stocks(originalPrice) values('%f')" % originalPrice)
    #c.execute("insert into stocks(discount) values('%f')" % discount)
    #c.execute("insert into stocks(saveMoney) values('%f')" % saveMoney)
    #c.execute("insert into stocks(soldNumber) values('%d')" % soldNumber)
    #c.execute("insert into stocks(sevenOrNot) values('%d')" % sevenOrNot)
    #c.execute("insert into stocks(expireOrNot) values('%d')" % expireOrNot)
    #c.execute("insert into stocks(validStartTime) values('%s')" % validStartTime)
    #c.execute("insert into stocks(validEndTime) values('%s')" % validEndTime)
    #c.execute("insert into stocks(tips) values('%s')" % strtips)
    #c.execute("insert into stocks(greatness) values('%s')" % strgreatness)
    #c.execute("insert into stocks(mainImage) values('%s')" % mainImage)

    
    conn.commit()
    c.close()
    


    







def main():
    baseUrl = "http://bj.meituan.com/"
    br = mechanize.Browser()
    data = br.open(baseUrl).get_data()
    links = scrapeLinks(baseUrl, data)
    links = rmRepeat(links)
    links = links[:len(links)-2]
   # print links
    for link in links:
        specificData = br.open(link).get_data()
        scrapeContents(specificData)


if __name__ == "__main__":
    main()
