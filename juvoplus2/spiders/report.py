#!/usr/local/bin/python3
# -*- coding: utf8 -*-
import sqlite3
import sys
from spiders.db import DB
import argparse


class Report(object):
    def __init__(self):
        self.conn = sqlite3.connect(DB.DATAFILE)

    def get_most_popular_gategories(self):
        gategories = []
        SQL = "select category_name from category"
        c = self.conn.cursor()
        for row in c.execute(SQL):
            gategories.append(row[0])
        return gategories


def get_args(args):
    '''
    ./report.py -U # list all use cases
    ./report.py -u [use case]
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-U', dest='list_usecases', action='store_true', default=False)
    parser.add_argument('-u', dest='usecases', nargs='*', type=int, default=[])
    return parser.parse_args(args)


def main():
    args = get_args(sys.argv[1:])
    print(args)


if __name__ == "__main__":
    main()