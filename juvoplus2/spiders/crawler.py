# -*- coding: utf8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
from spiders.db import YahooSQLite


class YahooCrawler(scrapy.Spider):
    name = 'Yahoo'
    start_urls = ['https://tw.buy.yahoo.com/catalog/ajax/recmdHotNew']

    def parse(self, response):
        self.init_db()

        res = json.loads(BeautifulSoup(response.body).text)
        bb = res['billboard']
        tabs = bb['tabs'] + bb['othertab']
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
            for pditem in panel['pditem']:
                pd_desc = pditem['desc']
                try:
                    pd_price = float(pditem['price'].replace('$', ''))
                except:
                    pd_price = -1
                self.insert_product(category_id, pd_desc, pd_price)
            counter += 1

    def init_db(self):
        ys = YahooSQLite()
        ys.destroy_db()
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
