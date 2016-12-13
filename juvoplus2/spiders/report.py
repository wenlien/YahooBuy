#!/usr/local/bin/python3
# -*- coding: utf8 -*-
import sqlite3
import sys
from spiders.db import DB, SCHEMA
import argparse


class UseCases:
    TOP_TWO_PER_CATEGORY = 'TOP_TWO_PER_CATEGORY'
    TOP_TEN_FOR_ALL = 'TOP_TEN_FOR_ALL'

    @staticmethod
    def get_use_cases():
        return [ use_case for use_case in dir(UseCases) if use_case[0:4] == 'TOP_']


class SortUpDown:
    ASC = 'asc'
    DESC = 'desc'

    @staticmethod
    def get_sort_cases():
        return [ SortUpDown.ASC, SortUpDown.DESC ]


class SQLStrategy:
    def __init__(self, usecase):
        self.usecase = usecase
        pass

    def get_SQL_by_usecase(self, sort_up_down=SortUpDown.DESC):
        if self.usecase == UseCases.TOP_TEN_FOR_ALL:
            SQL  = 'select c.category_name, p.product_name, p.price from %s as c, %s as p ' % (SCHEMA.CATEGORY, SCHEMA.PRODUCT)
            SQL += 'where 1 = 1 '
            SQL += '  and c.category_id = p.category_id '
            SQL += 'order by price %s ' % sort_up_down
            SQL += 'limit 10 '
        elif self.usecase == UseCases.TOP_TWO_PER_CATEGORY:
            SQL  = 'select c.category_name, p.product_name, p.price from %s as c, %s as p, ' % (SCHEMA.CATEGORY, SCHEMA.PRODUCT)
            SQL += '  (select product_id from %s where product_id %s 5 in (1, 2)) as t ' % (SCHEMA.PRODUCT, '%')
            SQL += 'where 1=1 '
            SQL += '  and p.product_id = t.product_id '
            SQL += '  and c.category_id = p.category_id '
            SQL += 'order by c.category_id, p.price %s ' % sort_up_down
        return SQL


class Report(object):
    def __init__(self, sort_up_down=SortUpDown.DESC):
        self.conn = sqlite3.connect(DB.DATAFILE)
        self.sort_up_down = sort_up_down

    def print_report(self, usecase):
        SQL = SQLStrategy(usecase).get_SQL_by_usecase(self.sort_up_down)
        c = self.conn.cursor()
        for (category_name, product_name, price) in c.execute(SQL):
            print("%s | %s | $%s" % (category_name, product_name, price if price != -1 else 'special price'))


def get_arg_parser():
    '''
    ./report.py -U # list all use cases
    ./report.py -u [use case] # apply use case
    ./report.py -s [sort] # apply sort
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-U', dest='list_usecases', action='store_true', default=False, help='List Usecases')
    parser.add_argument('-u', dest='usecases', type=str, default='', help='Apply Usecase')
    parser.add_argument('-s', dest='sort_up_down', type=str, default=SortUpDown.DESC, help='Apply sort sequence (%s/%s), default is %s' % (SortUpDown.ASC, SortUpDown.DESC, SortUpDown.DESC))
    return parser


def get_args(args):
    return get_arg_parser().parse_args(args)


def is_valid_args(args):
    if args.usecases not in UseCases.get_use_cases():
        print('Invalid use case (%s)!' % args.usecases)
        get_arg_parser().print_usage()
        exit(1)
    elif args.sort_up_down not in SortUpDown.get_sort_cases():
        print('Invalid sort argument (%s)!' % args.sort_up_down)
        get_arg_parser().print_help()
        exit(1)


def main():
    args = get_args(sys.argv[1:])
    if args.list_usecases:
        for use_case in UseCases.get_use_cases():
            print(use_case)
    elif args.usecases:
        is_valid_args(args)
        report = Report(args.sort_up_down)
        report.print_report(args.usecases)


if __name__ == "__main__":
    main()