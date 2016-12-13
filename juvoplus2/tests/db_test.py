# -*- coding: utf8 -*-
import unittest
from spiders.db import YahooSQLite


class DbTest(unittest.TestCase):
    def setUp(self):
        self.db = YahooSQLite()
        self.db.destroy_db()

    def test_create_db(self):
        self.assertFalse(self.db.is_init())

    def test_init_db(self):
        self.db.init_schema()
        self.assertTrue(self.db.is_init())

    def test_init_data(self):
        self.db.init_schema()
        self.db.insert_category("C1")
        self.db.insert_category("C2")
        self.db.insert_product(1, "P1", 100)
        self.db.insert_product(1, "P2", 200)
        self.db.query_category_data()
        self.db.query_product_data()
        self.db.query_category_product()

    def test_get_category_id_by_name(self):
        self.db.init_schema()
        self.db.insert_category("C1")
        self.db.insert_category("C2")
        self.db.insert_category("C3")
        self.assertEqual(self.db.query_category_id_by_name("C1"), 1)
        self.assertEqual(self.db.query_category_id_by_name("C2"), 2)
        self.assertEqual(self.db.query_category_id_by_name("C3"), 3)
