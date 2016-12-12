import sys
sys.path.insert(0, '../')
import unittest
from spiders.report import Report


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.report = Report()

    def test(self):
        print(self.report.get_most_popular_gategories())
