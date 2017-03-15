import requests
import urllib.request
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import os
import logging
import logging.handlers
import json
from config import Config
from filter import Filter
import hashlib

CONF_PATH = '../conf/config.ini'

class crawler():
    def __init__(self):
        self.news_data = []
        self.config = Config(CONF_PATH)

        self.logger = self.create_logger()

        self.filter = {}
        self.filter[self.config.get('filter1', 'name')] = Filter(self.config.get('filter1', 'file'))
        self.filter[self.config.get('filter2', 'name')] = Filter(self.config.get('filter2', 'file'))

        self.home = self.config.get('main', 'home')
        self.data = self.config.get('main', 'data')
        self.wait = float(self.config.get('main', 'sleep_wait'))
        self.max_page = int(self.config.get('main', 'max_page'))
        self.start = self.config.get('main', 'start')
        self.day = int(self.config.get('main', 'day'))
        self.total_cnt = 0
        self.success_cnt = 0
        self.start_day = 0
        self.end_day = 0

    def create_logger(self):
        logger = logging.getLogger(self.config.get('log', 'name'))
        formatter = logging.Formatter("[%(levelname)s|%(asctime)s] %(message)s")
        fileHandler = logging.FileHandler(self.config.get('log', 'file'))
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)

        if self.config.get('log', 'file') is 'info':
            logger.setLevel(logging.INFO)
        elif self.config.get('log', 'file') is 'debug':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        return logger

    def get_news(self, link, news_class, fp, csv_fp):
        try:
            res = requests.get(link)
        except:
            return False
        # soup = BeautifulSoup(res.content)
        soup = BeautifulSoup(res.content, "html.parser")

        try:
            title = soup.find('h3', attrs={"id": "articleTitle"}).get_text().strip()
            title = self.filter['string'].multiple_replace(title)

            content = soup.find('div', attrs={"id": "articleBodyContents"}).get_text().strip()
            content = self.filter['string'].multiple_replace(content)
            
            inputTag = soup.find('meta', attrs={"property": "me2:category1"})
            press = inputTag['content']
            
            written_time = soup.find('span', attrs={"class": "t11"}).get_text().strip()
            written_time = self.filter['date'].multiple_replace(written_time)

            comment_cnt = soup.find('span', attrs={"class": "lo_txt"}).get_text().strip()

            hash_object = hashlib.md5((title).encode())
            pk = str(hash_object.hexdigest())

            data = {'pk': pk, 'link': link, 'title': title, 'written_time': written_time, 'content': content, 'comment_cnt': comment_cnt, 'press': press, 'class': news_class}

            # self.es.index(index=self.config.get('es', 'index'), doc_type=self.config.get('es', 'doc_type'), body=data)
            fp.write(json.dumps(data, ensure_ascii=False) + '\n');

            csv_fp.write("\"" + data["pk"] + "\",")
            csv_fp.write("\"" + data["link"] + "\",")
            csv_fp.write("\"" + data["title"] + "\",")
            csv_fp.write("\"" + data["written_time"] + "\",")
            csv_fp.write("\"" + data["content"] + "\",")
            csv_fp.write("\"" + data["comment_cnt"] + "\",")
            csv_fp.write("\"" + data["press"] + "\",")
            csv_fp.write("\"" + data["class"] + "\"\n")
            self.success_cnt += 1
        except:
            self.logger.info('ERR ON '+ link)
            return False

        return True

    def get_news_class(self, news_class, url):
        if self.start == '':
            date_list = [datetime.now() - timedelta(days=x) for x in range(1, self.day + 1)]
        else:
            date_list = [datetime(int(self.start[0:4]), int(self.start[4:6]), int(self.start[6:8])) - timedelta(days=x) for x in range(1, self.day + 1)]

        self.start_day = date_list[len(date_list) - 1].strftime('%Y-%m-%d')
        self.end_day = date_list[0].strftime('%Y-%m-%d')

        link_list = set([])
        data_list = []
        self.logger.info(date_list)
        for date in date_list:
            page = 0
            flag = True
            today = date.strftime('%Y%m%d')
            directory_path = date.strftime('%Y-%m-%d')
            fp = open(self.data + '/' + self.config.get('filelist', 'crawl_result'), 'a', encoding='utf8')
            csv_fp = open(self.data + '/' + self.config.get('filelist', 'crawl_csv_result'), 'a', encoding='utf8')

            csv_fp.write("\"pk\",")
            csv_fp.write("\"link\",")
            csv_fp.write("\"title\",")
            csv_fp.write("\"writtentime\",")
            csv_fp.write("\"content\",")
            csv_fp.write("\"commentcnt\",")
            csv_fp.write("\"press\",")
            csv_fp.write("\"class\"\n")
 
            while(flag):
                page += 1

                if page > self.max_page:
                    break

                self.logger.info('class : ' + news_class + ', date : ' + today + ', page : ' +str(page))
                
                crawl_flag = False
                retry = 0
                while crawl_flag is False and retry < 10 and flag is True:
                    try:
                        res = requests.get(url%(today,page))
                        data = res.text
                        data = data.replace('\t','')
                        soup = BeautifulSoup(data)
                    
                        if page != 1:
                            old_list = list(data_list)

                        data_list = soup.find_all('div', class_='newsflash_body')[0].find_all('li')

                        if page != 1:
                            count = 0
                            for data in data_list:
                                if data in old_list:
                                    count += 1

                            if len(data_list) == count:
                                flag = False
                                break

                        self.logger.info('page\t: ' + url%(today,page))
                        crawl_flag = True
                    except:
                        self.logger.info("reload\t: " + url%(today,page) + ' ... ' + str(retry))
                        retry = retry + 1
                        crawl_flag = False

                    time.sleep(self.wait * 2)

                for data in data_list:
                    link = data.find_all('a')[0]['href']
                    link_list.add(link)

                for link in link_list:
                    retry = 0
                    crawl_flag = False
                    
                    self.total_cnt += 1
                    while crawl_flag is not True and retry < 3 :
                        self.logger.info("link\t: " + link + " retry : " + str(retry))
                        retry = retry + 1
                        crawl_flag = self.get_news(link, news_class, fp, csv_fp)
                        time.sleep(self.wait)
                
                
            # self.content_save2(today, news_class, directory_path.split('-'))
                link_list = set([])

            # self.report_to_slack2(today)
            fp.close()
            csv_fp.close()
    def get_politics(self):
        news_class = 'politics'
        url = 'http://news.naver.com/main/list.nhn?sid2=269&sid1=100&mid=shm&mode=LS2D&date=%s&page=%s' 
        self.get_news_class(news_class, url)

    def get_economy(self):
        news_class = 'economy'
        url = 'http://news.naver.com/main/list.nhn?sid2=263&sid1=101&mid=shm&mode=LS2D&date=%s&page=%s' 
        self.get_news_class(news_class, url)

    def get_it(self):
        news_class = 'it'
        url = 'http://news.naver.com/main/list.nhn?sid2=230&sid1=105&mid=shm&mode=LS2D&date=%s&page=%s' 
        self.get_news_class(news_class, url)

    def get_social(self):
        news_class = 'social'
        url = 'http://news.naver.com/main/list.nhn?sid2=257&sid1=102&mid=shm&mode=LS2D&date=%s&page=%s' 
        self.get_news_class(news_class, url)

    def get_culture(self):
        news_class = 'culture'
        url = 'http://news.naver.com/main/list.nhn?sid2=245&sid1=103&mid=shm&mode=LS2D&date=%s&page=%s' 
        self.get_news_class(news_class, url)

    def get_science(self):
        news_class = 'science'
        url = 'http://news.naver.com/main/list.nhn?sid2=228&sid1=105&mid=shm&mode=LS2D&date=%s&page=%s' 
        self.get_news_class(news_class, url)

    def get_global(self):
        news_class = 'global'
        url = 'http://news.naver.com/main/list.nhn?sid2=322&sid1=104&mid=shm&mode=LS2D&date=%s&page=%s' 
        self.get_news_class(news_class, url)

    def processing(self):
        try:
            targets = self.config.get('main', 'target').split('|')
            print(targets)

            for target in targets:
                if target.strip() == 'politics':
                    self.get_politics()
                elif target.strip() == 'economy':
                    self.get_economy()
                elif target.strip() == 'it':
                    self.get_it()
                elif target.strip() == 'social':
                    self.get_social()
                elif target.strip() == 'culture':
                    self.get_culture()
                elif target.strip() == 'science':
                    self.get_science()
                elif target.strip() == 'global':
                    self.get_global()
                else:
                    continue
            self.report_to_slack(self.config.get('main', 'target'))
        except:
            self.logger.info("error")

if __name__ == '__main__':
    crawler = crawler()
    crawler.processing()

