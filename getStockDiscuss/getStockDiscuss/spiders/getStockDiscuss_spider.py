# -*- coding: utf-8 -*-

import scrapy
import urllib

import sys
from selenium.common.exceptions import NoSuchElementException
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.closespider import CloseSpider

from pymongo import MongoClient
from selenium import webdriver
import time
import re
from urlparse import urlparse, parse_qs

from getStockDiscuss.items import GetStockDiscussItem

class getStockDiscussSpider(CrawlSpider):
    
    print " >>>>> >>>>> >>>> stockInfo crawler start"

    def __init__(self, *args, **kwargs):
        stockNo = '263800'
        self.curUrl = 'http://finance.naver.com/item/board.nhn?code=018260&page='
#         self.curUrl = 'http://m.stock.naver.com/item/main.nhn#/stocks/005930/discuss'
        self.error_code = 0;
        self.parameter = kwargs.get('p_args')
        print ">>>>> url: ", self.curUrl
        self.driver = webdriver.Firefox(executable_path=r'C:\Users\developer\geckodriver.exe')
        self.start_urls = [self.curUrl]
        
        
        super(getStockDiscussSpider, self).__init__(*args, **kwargs)
 
    name = 'getStockDiscuss'
 
    def parse(self, response):
 
        print ">>>>> parse start"
        
        if(self.error_code == 1):
            print ">>>>> error:", 'one of mandatory arguments is not retrieved'
            raise CloseSpider()
        
        def frange(start, stop, step):
            i = start
            while i < stop:
                yield i
                i += step
                
        curNo = 1
        while True:
            try:
                print 'url: ', response.url + str(curNo)
                self.driver.get(response.url + str(curNo))

                hxs = Selector(text=self.driver.page_source)
                iteratedObjectLiXPath = "//table/tbody/tr"
                objects = hxs.xpath(iteratedObjectLiXPath)
                
                
                for o in objects:
                    if(len(o.xpath('td/span/text()')) != 0):
                        if(o.xpath('td/span/text()')[0].extract() != '전일' and o.xpath('td/span/text()')[0].extract() != '시가'
                           and o.xpath('td/span/text()')[0].extract() != 'l' and len(o.xpath('td/span/text()')) > 2):
                            date = o.xpath('td/span/text()')[0].extract().strip()
                            opinion = o.xpath('td/span/text()')[1].extract().strip()
                            count = o.xpath('td/span/text()')[2].extract().strip()
                            author = o.xpath('td/text()')[1].extract().strip()
                            title = o.xpath('td/a/text()')[0].extract().strip()
                            url = o.xpath('td/a/@href')[0].extract()
                            query = urlparse(url).query
                            params = parse_qs(query)
                            nid = params.get("nid")[0].strip()
                            print 'date: ', date, ', title: ', title, ', author: ', author, 'count: ', count, ', opinion: ', opinion, ', nid: ', nid
                
                for i in frange(0.5, 1.0, 0.1):
                    time.sleep(1)
                    
                curNo = curNo + 1
                
            except NoSuchElementException:
                break
            
        self.driver.close()
