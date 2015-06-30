#coding=utf-8
import mechanize
from bs4 import BeautifulSoup
import re
import urllib
import wget
import os

br = mechanize.Browser()
STATIC_ROOT = os.path.join(os.path.dirname(__file__),'../image/')

def get_page(url):
    try:
        html = br.open(url)
        soup = BeautifulSoup(html.read())
        table = soup.findAll('table',{'bgcolor':'#FFFFFF'})
        for table_td in table:
            tds = table_td.find('td')
            return tds.renderContents().split('|')[1].replace('共','').replace('页','')
    except Exception,e:
        print e
        raise e

def get_title(url):
    try:
        html = br.open(url)
        soup = BeautifulSoup(html.read())
        title = soup.title
        return title
    except Exception,e:
        print e
        raise e
    

def get_down_url(url):
    try:
        print u'进入网址下载页'     
        html = br.open(url)
        soup = BeautifulSoup(html.read())
        text = soup.find_all('a')
        li = []
        
        for str in text:
            stri =  str.get('href')
            stri = re.findall('/comiclist/2055/(.*)',stri.__repr__())
            if stri:
                li.append(stri[0].replace("'",''))
     
        for url in list(set(li)):
            filename =  url.split('/')[0]
            if url != 'index.htm':
                title_url = 'http://comic.kukudm.com/comiclist/2055/' + filename + '/' +'1.htm'
                page = get_page(title_url)
                url_title = get_title(title_url).string
                title = unicode(url_title).encode('utf-8')
                print title
            for page in range(1,int(page)+1):
                page = bytes(page)
                url = 'http://comic.kukudm.com/comiclist/2055/' + filename + '/' + page +'.htm'
                if not os.path.isdir(title):
                    if filename != 'index.htm':
                        print u'创建文件夹     ' + url_title
                        os.makedirs(title)
                        get_image_url(url,title + '_' + page)
                get_image_url(url,title + '_' + page)
    except Exception,e:
        print e
        raise e
        
def get_image_url(url,title):
    try:
        print u'进入图片网址下载页'
        m201304d='http://n.kukudm.com/'
        html = br.open(url)
        soup= BeautifulSoup(html.read())
        url_end = soup.find_all('script')[3].string.split('SRC=')[1].split("'><span style='display:none'>")[0].split("+m201304d+")[1].replace('"','')
        url = m201304d + url_end
        save_image(url,title)
    except Exception,e:
        print e


def save_image(url,title):
    print u'开始下载图片'
    url = url.encode('utf-8')
#     urllib.urlretrieve(url,os.path.join(title,os.path.basename(title)))
    save_image_url = os.path.join(os.path.dirname(__file__) ,os.path.join(title,os.path.basename(title)))
    print save_image_url
    with open(save_image_url,'wb') as f:
        f.write(title)
        print title + u'下载完成'

if __name__ == '__main__':
    try:
        url = 'http://comic.kukudm.com/comiclist/2055/index.htm'
        get_down_url(url)
    except Exception,e:
        print e
        raise e