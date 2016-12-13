# -*- coding: utf8 -*-
import sqlite3
import os


class DB:
    DATAFILE = '/tmp/sqlite.db'


class SCHEMA:
    CATEGORY = 'category'
    PRODUCT = 'product'
    CREATE_CATEGORY = 'CREATE TABLE %s(category_id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT);' % CATEGORY
    CREATE_PRODUCT = 'CREATE TABLE %s(product_id INTEGER PRIMARY KEY AUTOINCREMENT, category_id INTEGER, product_name TEXT, price REAL);' % PRODUCT
    SELECT_CATEGORY = 'SELECT * FROM %s' % CATEGORY
    SELECT_PRODUCT = 'SELECT * FROM %s' % PRODUCT
    SELECT_CATEGORY_PRODUCT = 'SELECT c.category_name, p.product_name, p.price FROM %s as c, %s as p WHERE c.category_id = p.category_id' % (CATEGORY, PRODUCT)
    SELECT_CATEGORY_ID_BY_NAME = 'SELECT category_id FROM %s WHERE category_name="%s"' % (CATEGORY, "%s")
    INSERT_CATEGORY = 'INSERT INTO %s(category_name) VALUES("%s")' % (CATEGORY, "%s")
    INSERT_PRODUCT = 'INSERT INTO %s(category_id, product_name, price) VALUES(%s, "%s", %s)' % (PRODUCT, "%s", "%s", "%s")


class SQLType:
    DDL = 0
    DML = 1


class YahooSQLite(object):
    def __init__(self):
        pass

    def destroy_db(self):
        if os.path.exists(DB.DATAFILE):
            os.remove(DB.DATAFILE)
        print('destroy db done!')

    def get_conn(self):
        return sqlite3.connect(DB.DATAFILE)

    def run_SQL(self, SQL, sql_type):
        print(SQL)
        conn = self.get_conn()
        c = conn.cursor()
        if sql_type == SQLType.DML:
            rs = []
            for row in c.execute(SQL):
                rs.append(row)
        else:
            c.execute(SQL)
            rs = None
        # print(rs)
        conn.commit()
        conn.close()
        return rs

    def run_DML(self, SQL):
        return self.run_SQL(SQL, SQLType.DML)

    def run_DDL(self, SQL):
        self.run_SQL(SQL, SQLType.DDL)
        return None

    def is_init(self):
        # print(os.path.exists(DB.DATAFILE))
        try:
            if os.path.exists(DB.DATAFILE) and self.run_DML(SCHEMA.SELECT_PRODUCT) is not None:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def init_schema(self):
        self.run_DDL(SCHEMA.CREATE_CATEGORY)
        self.run_DDL(SCHEMA.CREATE_PRODUCT)
        print('init schema done!')

    def insert_category(self, category_name):
        self.run_DML(SCHEMA.INSERT_CATEGORY % category_name)

    def insert_product(self, category_id, product_name, price):
        self.run_DML(SCHEMA.INSERT_PRODUCT % (category_id, product_name, price))

    def insert_many(self, name_price_list):
        for name, price in name_price_list:
            self.insert_product(name, price)

    def print_result_set(self, SQL):
        for row in self.run_DML(SQL):
            for data in row:
                print('%s ' % data, end='')
            print('')

    def query_category_data(self):
        self.print_result_set(SCHEMA.SELECT_CATEGORY)

    def query_product_data(self):
        self.print_result_set(SCHEMA.SELECT_PRODUCT)

    def query_category_product(self):
        self.print_result_set(SCHEMA.SELECT_CATEGORY_PRODUCT)

    def query_category_id_by_name(self, category_name):
        category_id = None
        SQL = SCHEMA.SELECT_CATEGORY_ID_BY_NAME % category_name
        for row in self.run_DML(SQL):
            category_id = int(row[0])
        return category_id
