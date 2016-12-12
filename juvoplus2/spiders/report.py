import sqlite3
import sys
from .db import DB


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