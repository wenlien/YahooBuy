# -*- coding: utf8 -*-
import unittest
from spiders.report import Report, get_args


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.report = Report()

    def compare_args_result(self, args, result):
        res = get_args(args)
        self.assertEqual(res.list_usecases, result[0])
        self.assertEqual(res.usecases, result[1])

    def test_args(self):
        args = ['-U', '-u', '1', '2']
        self.compare_args_result(args, [True, [1, 2]])
        args = ['-u', '1', '2']
        self.compare_args_result(args, [False, [1, 2]])
        args = ['-U']
        self.compare_args_result(args, [True, []])
        args = []
        self.compare_args_result(args, [False, []])

    def test(self):
        print(self.report.get_most_popular_gategories())
