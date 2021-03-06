#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
抓取    alphacoders Wallpapers async
'''
import argparse
from cgitb import text
import os
import time
import requests
import sys
from config import global_config
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import asyncio
import aiohttp
MAX_ASYN = 5
session = None
semaphore = asyncio.Semaphore(MAX_ASYN)
proxie = { 
    'http' : 'http://xx.xxx.xxx.xxx:xxxx',
    'http' : 'http://xxx.xx.xx.xxx:xxx',
    
}
PAGE_SIZE = 18
INDEX_URL='https://spa5.scrape.center/api/book/?limit=18&offset={offset}' 

import multiprocessing
#response = requests.get(url,proxies=proxies)

ua = UserAgent(verify_ssl=False, path='./fake.json')
pic_list = list();       
def random_ua():
    headers = {
        "user-agent": ua.random,
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection":"keep-alive",      
        "Upgrade-Insecure-Requests":"1"
    }
    return headers

class Crawler():
    def __init__(self,_delay):
        self.__keyword = str()
        self.__total_page = 5
        self.__time_sleep = _delay
        
    def geturl(self,url):
        try:
            r = requests.get(url, headers=random_ua())
            if r.status_code == 200:
                return  r.text
        except Exception as e:
            print(str(e))

    def parse(self,html):
        soup = BeautifulSoup(html,'lxml')
        clazz = soup.find_all(class_='img-responsive big-thumb')
        for cl in clazz:
            url = cl['src'].replace('thumbbig-','')
            pic_list.append(url)

    def save(self):
      
        if not os.path.exists("./" + self.__keyword):
            os.mkdir("./" + self.__keyword)
    
        # for count ,url in enumerate(pic_list):
        #     time.sleep(1)
        #     pic = requests.get(url,headers=random_ua()) # 发送请求
        #     if pic.status_code == 200:
                
        #         filename = "./" + self.__keyword+'/'+os.path.basename(url)
        #         print('saving %s ....'%(filename))
        #         with open (filename, 'wb') as f:
        #             f.write(pic.content)
        #             f.close()

        results = []
        pool = multiprocessing.Pool(processes = 20)
        scale = len(pic_list)
        for i ,url in enumerate(pic_list):
            a = "#"* int(i/10)
            b = "."*(int(scale/10)-int(i/10))
            c = (i/scale)*100
            results.append(pool.apply_async(self.get, (url,random_ua())))
            print('{:^3.3f}%[{}>>{}]'.format(c, a, b)) # 进度条（可用tqdm）
            
        pool.close()                        # 调用join之前，先调用close函数，否则会出错。
        pool.join()                         # join函数等待所有子进程结束
            
    def get(self,url,_headers):
        pic = requests.get(url,headers=_headers) # 发送请求
        if pic.status_code == 200:
            filename = "./" + self.__keyword+'/'+os.path.basename(url)
            print('saving %s ....'%(filename))
            with open (filename, 'wb') as f:
                f.write(pic.content)
                f.close()


    async def scrape_index(page):
        url = INDEX_URL.format(offset=PAGE_SIZE *(page-1))
        return await scrape_api(url)
        

    async def scrape_api(url):
        async with semaphore:
            try:
                print('scrape url ==> ',url)
                async with session.get(url) as response:
                    return await response.json()
            except Exception as e:
                print(e)
    async def main():
        global session
        session = aiohttp.ClientSession()
        tasks = [asyncio.ensure_future(scrape_index(i)) for i in range(1,5)]
        print('START gather')
        results = await asyncio.gather(*tasks)
        print('AFTER gather')
        #data = json.dumps(results,ensure_ascii=False,indent=2)
        ids = []
        for res in results:
            if not res : continue
            for item in res.get('results'):
                print(item.get('id'))
                ids.append(item.get('id'))
                
        #detail_tasks = [asyncio.ensure_future(scrape_datail(id)) for id in ids]
        #await asyncio.wait(detail_tasks)
        await session.close()
    def startasync():
      
    
        start = time.time()
        results = asyncio.get_event_loop().run_until_complete(main())
        end = time.time()

        print('total spend time ==> ',end-start)


    def start(self,word = 'space',total_page = 60):
        self.__keyword = word
        self.__total_page = total_page + 2
        for i in range(2, self.__total_page):
            time.sleep(self.__time_sleep)
            xurl = 'https://wall.alphacoders.com/search.php?search=%s&lang=Chinese&quickload=4096&page=%d'%(self.__keyword,i)
            print('downloading %s ....'%(xurl))
            html = self.geturl(xurl)
            self.parse(html)
        self.save()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--word", type=str, help="抓取关键词", required=True)
        parser.add_argument("-tp", "--total_page", type=int, help="需要抓取的总页数", rdefault=3)
        parser.add_argument("-d", "--delay", type=float, help="抓取延时（间隔）", default=0.05)
    
        args = parser.parse_args()
        crawler = Crawler(args.delay)
        crawler.start(args.word, args.total_page)  # 抓取关键词为 args.word ，总数为 args.total_page页
    else:
        crawler = Crawler(0.1)  # 抓取延迟为 0.05
        crawler.start()  # 抓取关键词为 “comic”，总数为 1 页
      
