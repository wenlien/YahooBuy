#!/usr/local/bin/python3
# -*- coding: utf8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
# import codecs
# import sys
# UTF8Writer = codecs.getwriter('utf8')
# sys.stdout = UTF8Writer(sys.stdout)
from .db import YahooSQLite


class YahooCrawler(scrapy.Spider):
    name = 'Yahoo'
    # start_urls = ['https://tw.buy.yahoo.com/catalog/ajax/recmdHotNew']
    start_urls = ['https://tw.buy.yahoo.com/catalog/ajax/recmdHotNew?segmentId=999999&subId=24,10,28,30,478,90,464,35,536,613&t=1481549824762']

    def parse(self, response):
        self.init_db()

        res = json.loads(BeautifulSoup(response.body).text)
        bb = res['billboard']
        tabs = bb['tabs'] + bb['othertab']
        # for tab in tabs:
        #     print(tab['label'])
        panels = bb['panels']

        counter = 0
        for panel in panels:
            category_name = tabs[counter]['label']
            self.insert_category(category_name)
            category_id = self.get_category_id_by_name(category_name)

            mainitem = panel['mainitem']
            main_desc = mainitem['desc']
            try:
                main_price = float(mainitem['price'].replace('$', ''))
            except:
                main_price = -1
            self.insert_product(category_id, main_desc, main_price)
            # print(u'%s: %s' % (main_desc, main_price))
            for pditem in panel['pditem']:
                pd_desc = pditem['desc']
                try:
                    pd_price = float(pditem['price'].replace('$', ''))
                except:
                    pd_price = -1
                self.insert_product(category_id, pd_desc, pd_price)
                # print(u'%s: %s' % (pd_desc, pd_price))
            counter += 1

    def init_db(self):
        ys = YahooSQLite()
        if not ys.is_init():
            ys.init_schema()

    def insert_category(self, category_name):
        ys = YahooSQLite()
        ys.insert_category(category_name)

    def insert_product(self, category_id, product_name, price):
        ys = YahooSQLite()
        ys.insert_product(category_id, product_name, price)

    def get_category_id_by_name(self, category_name):
        ys = YahooSQLite()
        return ys.query_category_id_by_name(category_name)
