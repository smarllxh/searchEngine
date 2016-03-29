# coding=utf-8
import urllib2
from BeautifulSoup import *
from urlparse import urljoin

import pymysql
import jieba


class crawler:
    def __init__(self,dbname):
        self.conn=pymysql.connect(host='localhost',port=3306,user='root',db=dbname,passwd='32784744li')

        self.cur=self.conn.cursor()
    #page is a list
    def creattables(self):
        try:
            self.cur.execute('create table wordlist(rowid int auto_increment primary key,word varchar(255))')
            self.cur.execute('create table urlist(rowid int auto_increment primary key,url varchar(255))')
            self.cur.execute('create table wordlocation(rowid int primary key auto_increment,wordid int,urlid int,location int)')
            self.cur.execute('create table link(rowid int auto_increment primary key,fromid int,toid int)')
            self.cur.execute('create table linkword(rowid int auto_increment primary key,wordid int,linkid int)')
        except Exception,e:
            print e.message
            print "can not create tables\n"

    def crawler(self,pages,depth):

        for i in range(depth):
            pagelist=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                    soup=BeautifulSoup(c.read())
                except :
                    print page
                    continue
                self.addtoindex(page,soup)
                for a in soup('a'):
                    if ('href' in dict(a.attrs)):
                        link=a['href']
                        if link[0:4]!='http':
                            link=urljoin(page,link)
                        pagelist.add(link)
                        print link
            pages=pagelist

    def gettextonly(self,soup):

        v=soup.string
        if v==None:
            finalresult=""
            for c in soup.contents:
                subresult=self.gettextonly(c)
                finalresult+=subresult

            return finalresult
        else:
            return v.strip()

    def seperatewords(self,text):
       string=''
       for word in text.split('\n'):
           string+=word+'\n'
       print string
       string = jieba.cut(text)
       #print "_".join(word)
            #print word+str('this is onw word\n\n\n\n\n\n\n')

    def addtoindex(self,page,soup):
        urlid=self.getentryid('urlist','url',page)
        text= self.gettextonly(soup)
        words=self.seperatewords(text)
        for i in range(len(words)):
            wordid=self.getentryid('wordlist','word',words[i].encode('utf-8'))
            self.cur.execute("insert into wordlocation values(Null,'%s','%s')" % wordid,urlid,i)
            self.conn.commit()

    def getentryid(self,table,field,value):
           #print "select rowid from %s where %s = '%s' " % (table,field,value)
           self.cur.execute("select rowid from %s where %s = '%s' " % (table,field,value))
           row=self.cur.fetchone()
           if row==None:
               self.cur.execute("insert into %s set %s='%s' " % (table,field,value))
               self.conn.commit()
               return self.cur.lastrowid
           else:
               return row[0]


class searcher:
    def __init__(self,dbname):
        self.con=pymysql.connect(host='localhost',port=3306,user='root',password='32784744li',db=dbname)
    def getmatchrows(self):
        pass
    def getscoredlist(self):
        pass

craw=crawler('searchengine')
#craw.creattables()
u=urllib2.urlopen('http://www.njupt.edu.cn')
soup=BeautifulSoup(u.read())
print soup.get_starttag_text()
#print craw.gettextonly(soup)
#craw.crawler(['https://www.douban.com'],2)
#craw.creattables()
#print craw.getentryid('wordlist','word','lixianljjsfdsfsljlk')
#text=craw.gettextonly(soup)
#craw.addtoindex('http://www.crummy.com/software/BeautifulSoup/bs4/doc/',soup)
#craw.seperatewords(text)
