# -*- coding: utf8 -*-
import unittest
from spiders.report import Report, get_args, SQLStrategy, UseCases


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.report = Report()

    def compare_args_result(self, args, result):
        res = get_args(args)
        print(res)
        self.assertEqual(res.list_usecases, result[0])
        self.assertEqual(res.usecases, result[1])

    def test_args(self):
        args = ['-U', '-u', UseCases.TOP_TEN_FOR_ALL]
        self.compare_args_result(args, [True, UseCases.TOP_TEN_FOR_ALL])
        args = ['-u', UseCases.TOP_TWO_PER_CATEGORY]
        self.compare_args_result(args, [False, UseCases.TOP_TWO_PER_CATEGORY])
        args = ['-U']
        self.compare_args_result(args, [True, ''])
        args = []
        self.compare_args_result(args, [False, ''])

    def test_SQL_Strategy(self):
        ss = SQLStrategy(UseCases.TOP_TEN_FOR_ALL)
        print(ss.get_SQL_by_usecase())
        ss = SQLStrategy(UseCases.TOP_TWO_PER_CATEGORY)
        print(ss.get_SQL_by_usecase())
        ss = SQLStrategy(UseCases.TOP_TEN_FOR_ALL)
        print(ss.get_SQL_by_usecase())
        ss = SQLStrategy(UseCases.TOP_TWO_PER_CATEGORY)
        print(ss.get_SQL_by_usecase())
